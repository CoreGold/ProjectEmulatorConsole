import requests
from bs4 import BeautifulSoup
import argparse
import graphviz


def get_dependencies(package_name):
    url = f"https://pkgs.alpinelinux.org/package/edge/main/x86_64/{package_name}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Ошибка при получении данных для пакета {package_name}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    dependencies = []
    depends_section = soup.find('summary', string=lambda text: text and 'Depends' in text)

    if depends_section:
        ul = depends_section.find_next('ul')
        if ul:
            for li in ul.find_all('li'):
                dep = li.text.strip()
                if dep.startswith("so:"):
                    dep = dep[3:]
                    dep = dep.split('.')[0]

                if dep and dep not in dependencies:
                    dependencies.append(dep)

    return dependencies


def create_dependency_graph(package_name, output_file, visited=None):
    if visited is None:
        visited = set()

    dependencies = get_dependencies(package_name)

    graph = graphviz.Digraph(format='png')

    for dep in dependencies:
        if dep not in visited:
            visited.add(dep)
            graph.node(package_name)
            graph.node(dep)
            graph.edge(package_name, dep)

            sub_dependencies = get_dependencies(dep)
            for sub_dep in sub_dependencies:
                graph.edge(dep, sub_dep)
                create_dependency_graph(sub_dep, output_file, visited)

    # Сохранение графа в файл
    graph.render(output_file, cleanup=True)
    print(f"Граф зависимостей сохранен в {output_file}.png")
    print("Визуализация завершена успешно!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', required=True,)
    parser.add_argument('--output-file', required=True,)

    args = parser.parse_args()

    create_dependency_graph(args.package, args.output_file)


if __name__ == "__main__":
    main()
