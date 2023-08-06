import json
import subprocess
from pathlib import Path
from threading import Lock
from datetime import datetime
from functools import partial
from urllib.parse import urljoin
from multiprocessing.pool import ThreadPool

import toml
import requests

# utils


def create_session(pool_maxsize, max_retries=10):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_maxsize=pool_maxsize, max_retries=max_retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def read_know_resources():
    p_know_resources = Path("know_resources.json")

    if p_know_resources.is_file():
        with p_know_resources.open() as f:
            know_resources = json.load(f)
    else:
        know_resources = {}

    return know_resources


def write_know_resources(item, status):
    p_know_resources = Path("know_resources.json")
    know_resources = read_know_resources()

    know_resources[item["resource_id"]] = {
        "status": status,
        "resource_revision_id": item["resource_revision_id"],
        "resource_last_modified": item["resource_last_modified"],
    }

    with p_know_resources.open("w") as f:
        json.dump(know_resources, f, indent=2, sort_keys=True, ensure_ascii=False)


def parse_date(date: str) -> datetime:
    """Util to parse """
    try:
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

def print_out_err(cmd):
    if cmd.stdout:
        print(cmd.stdout.decode())
    if cmd.stderr:
        print(cmd.stderr.decode())


def git_add_commit(files, msg):
    cmd_git_add = subprocess.run(["git", "add"] + files, stderr=subprocess.PIPE)
    print_out_err(cmd_git_add)

    cmd_git_commit = subprocess.run(["git", "commit", "-m", f"'{msg}'"], stderr=subprocess.PIPE)
    print_out_err(cmd_git_commit)


def git_push():
    cmd_git_push = subprocess.run(["git", "push"], stderr=subprocess.PIPE)    
    print_out_err(cmd_git_push)


# end utils


def get_package_list(base_url, session):
    """Get a list of all the names of the posibles packages"""
    url_package_list = urljoin(base_url, "package_list")
    r = session.get(url_package_list)
    package_list = r.json()["result"]
    return package_list


def get_package_metadata(url, session, package):
    """Download a single package's metadata"""
    r = session.get(url, params={"id": package})
    result = r.json()["result"]

    p_package = Path("data") / package
    p_package.mkdir(exist_ok=True)

    # TODO: ordenar el dump y separa en lineas para hacer mas trackeable por git
    with (p_package / "package_show.json").open("w") as f:
        json.dump(result, f, indent=2, sort_keys=True, ensure_ascii=False)

    items_resource = []

    for resource in result["resources"]:
        item_resouce = {
            "package_name": package,
            # "package_path": p_package,
            "package_id": resource["package_id"],
            "resource_path": Path(package) / resource["url"].rsplit("/", maxsplit=-1)[-1],
            "resource_id": resource["id"],
            "resource_url": resource["url"],
            "resource_type": resource["resource_type"],
            "resource_format": resource["format"],
            "resource_revision_id": resource["revision_id"],
            "resource_last_modified": resource["last_modified"]
            }    
        items_resource.append(item_resouce)

    return items_resource


def get_packages_metadata(base_url, session, package_list, num_threads):
    """Download save and return metadata from all package_list"""
    url_package_show = urljoin(base_url, "package_show")
    partial_get_package_metadata = partial(get_package_metadata, url_package_show, session)

    with ThreadPool(num_threads) as pool:
        all_resources = pool.map(partial_get_package_metadata, package_list)

    all_resources = [
        item for items_resource in all_resources for item in items_resource
        ]
    # comiteamos todos los metadatos
    git_add_commit(["data"], "update pacakge_show.json")
    git_push()

    return all_resources


def find_resources_to_download(all_resources):
    know_resources = read_know_resources()

    # TODO: check if any resource have a duplicate id (and print a warning)
    new_items = []
    updated_items = []
    for item in all_resources:
        item_resource_id = item["resource_id"]
        if item_resource_id in know_resources and know_resources[item_resource_id]["resource_revision_id"] != item["resource_revision_id"]:
            updated_items.append(item)
        # TODO: check if resource_type == document
        elif item["resource_type"] == "file":
            new_items.append(item)
        else: 
            continue  # TODO: agregarlos al know_resources con la razon!

    return new_items, updated_items


def get_single_resource_and_commit(session, lock, item):
    url = item["resource_url"]
    p_know_resources = Path("know_resources.json")
    p_data_file = Path("data") / item["resource_path"] 
    p_tmp_file = Path("tmp") / item["resource_path"]
    p_tmp_file.parent.mkdir(exist_ok=True)

    if not url:
        with lock:
            write_know_resources(item, status="not_valid_url")
            git_add_commit([p_know_resources], "Update know_resources.json")
            return

    try:
        with session.get(url, stream=True) as r:
            try:
                r.raise_for_status()
            except requests.HTTPError:
                print("HTTP error in resource ", item["resource_path"])
                with lock:
                    write_know_resources(item, status="http_error")
                    git_add_commit([p_know_resources], "Update know_resources.json")
                    return

            with p_tmp_file.open("wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    except requests.ConnectionError:
        print("Connection error in resource ", item["resource_path"])
        with lock:
            write_know_resources(item, status="connectoin_error")
            git_add_commit([p_know_resources], "Update know_resources.json")
            return  

    # miro el tamaño
    file_size = p_tmp_file.stat().st_size
    if file_size > 97_000_000:  # aprox 100MB
        # TODO: agregar formas de agarara estos archivos grandes (splitear/compirmir)
        p_tmp_file.unlink()
        print("Lo dropeamos por ser muy grande", item["resource_path"])
        with lock:
            write_know_resources(item, status="file_to_large")
            git_add_commit([p_know_resources], "Update know_resources.json")
            return

    p_tmp_file.rename(p_data_file)
    with lock:

        write_know_resources(item, status="ok")
        git_add_commit([p_know_resources, p_data_file], f"Update {p_data_file} and know_resources.json")
        git_push()
        print("Pium! lo comiteamos!")

        # comiteamos el cambio

    print("Archivo termino todo bien!", item["resource_path"])
    return   # TODO: return the new_know_resource_state

    
def get_resources_and_commit(session, items, num_threads):
    lock = Lock()
    partial_get_single_resources_and_commit = partial(get_single_resource_and_commit, session, lock)

    with ThreadPool(num_threads) as pool:
        pool.map(partial_get_single_resources_and_commit, items)


# utils for write the readme

# TODO: Solo poner en las que tenga algun resource (no dan info las apis por ej)
# TODO: Marcar diferentes los resources o paquetes que ya no estan mas en el portal (algo como archivados)
# TODO: marcar con un campo los recursos que al menos se bajaron una vez

def build_readme():
    # TODO: hacer todo un objeto y leerlo de un atributo
    path_data = Path("data")
    portal_metadata = toml.load("portal.toml")
    portal_title = portal_metadata["info"]["name"]
    portal_url = portal_metadata["info"]["url"]
    know_resources = read_know_resources()

    body = f"""# {portal_title}

Portal url: {portal_url}

"""
    
    list_packages_show = []
    for p in path_data.glob("*/package_show.json"):
        with p.open() as f:
            package_show = json.load(f)
            # filter only resources with 
            if any(resource_id in know_resources for resource_id in [resource["id"] for resource in package_show["resources"]]):
                list_packages_show.append(package_show)

    list_packages_show = sorted(list_packages_show, key=lambda x: x["title"])

    for package in list_packages_show:
        body += build_readme_package(package)
    
    return body

def build_readme_package(package_show):
    package_title = package_show["title"]
    package_author = package_show["author"]
    package_author_email = package_show["author_email"]
    if package_author_email:
        package_author = f"{package_author} [✉️](malito:{package_author_email})"
    package_notes = package_show["notes"]

    body = f""" ## {package_title}

Autor: {package_author}

{package_notes}

"""
    
    for resource in package_show["resources"]:
        body += build_readme_resource(resource, package_show["name"])
        
    return body

def build_readme_resource(resource, package_name):
    resource_name = resource["name"]
    resource_description = resource["description"]
    resource_file_name = resource["url"].rsplit("/", maxsplit=1)[-1]
    
    # TODO: hacer todo un objeto y leerlo de un atributo
    portal_metadata = toml.load("portal.toml")
    
    base_repo_url = portal_metadata["info"]["base_repo_url"]
    resource_download_url = f"{base_repo_url}/master/data/{package_name}/{resource_file_name}"
    
    # resource_attibutes_description = resource["attributesDescription"]
    # if resource_attibutes_description:
    #     resource_attibutes_description = json.loads(resource_attibutes_description)
        # TODO: hacer tabla y ponerla con el html para que sea desplegable.
    
    # TODO: ultima modificacion, fecha creacion, sha/hash, tipo de recurso link al recurso
    
    body = f""" ### {resource_name}

{resource_description}

[Download]({resource_download_url})

"""
    
    return body

# end utils


def main():
    num_threads = 10
    # leemos la metadata
    portal_metadata = toml.load("portal.toml")
    base_url = urljoin(portal_metadata["info"]["url"], "api/3/action/")

    Path("data").mkdir(exist_ok=True)
    Path("tmp").mkdir(exist_ok=True)

    session = create_session(pool_maxsize=num_threads, max_retries=10)
    # encontramos todos los paquetes
    package_list = get_package_list(base_url, session)
    # traemos la metadata de todos los paquetes (y la guardamos)
    all_resources = get_packages_metadata(base_url, session, package_list, num_threads)
    # encontramos que hay de nuevo
    new_items, updated_items = find_resources_to_download(all_resources)
    print("new items to download: ", len(new_items), "updated_items: ", len(updated_items))

    if new_items:
        print("Find: ", len(new_items), " new items.")
        get_resources_and_commit(session, new_items, num_threads)
        git_push()
        # TODO: actualizar el know_reosurces ids
    else:
        print("no new items to download.")

    if updated_items:
        print("Find: ", len(updated_items), " updated items.")
        get_resources_and_commit(session, updated_items, num_threads)
        git_push()
        # TODO: actualizar el know_reosurces ids
    else:
        print("No updated items to download.")

    # write readme.md
    with open("READNE.md", "w") as f:
        f.write(build_readme())


if __name__ == "__main__":
    main()
