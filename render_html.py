import os
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

DATA_DIR = "data"
OUTPUT_DIR = "site"
TEMPLATE_DIR = "templates"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template("release_template.html")

def load_release_data(filename):
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return json.load(f)

def render_repo_html(repo_json_file):
    repo_name = repo_json_file.replace(".json", "").replace("_", "/")
    releases = load_release_data(repo_json_file)

    output_html = template.render(
        repo_name=repo_name,
        releases=releases
    )

    safe_filename = repo_json_file.replace(".json", ".html")
    output_path = os.path.join(OUTPUT_DIR, safe_filename)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(output_html)
    print(f"✅ Rendered HTML for {repo_name} → {output_path}")

def generate_index_page(repo_files):
    """
    Generate index.html in the project root.
    """
    index_template = env.get_template("index.html")
    repo_links = []

    for filename in repo_files:
        name = filename.replace(".json", "").replace("_", "/")
        html_file = os.path.join("site", filename.replace(".json", ".html"))
        repo_links.append({
            "name": name,
            "filename": html_file
        })

    html = index_template.render(repos=repo_links)

    # Save to root
    with open("index.html", "w") as f:
        f.write(html)

    print("🏠 Homepage generated at ./index.html")

def generate_sitemap(repo_files, domain="https://yourdomain.com"):
    """
    Generate sitemap.xml in root, with links to all release pages and index.
    """
    urls = [f"{domain}/index.html"]  # Include homepage

    for file in repo_files:
        html_file = file.replace(".json", ".html")
        urls.append(f"{domain}/site/{html_file}")

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in urls:
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{url}</loc>")
        sitemap.append("  </url>")

    sitemap.append("</urlset>")

    with open("sitemap.xml", "w") as f:
        f.write("\n".join(sitemap))

    print("🗺️  Sitemap generated at ./sitemap.xml")

def main():
    # Collect all JSON files from the data directory
    repo_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

    # Render an HTML page per repo
    for filename in repo_files:
        render_repo_html(filename)

    # Generate the homepage (index.html)
    generate_index_page(repo_files)

    # Generate the sitemap (sitemap.xml)
    generate_sitemap(repo_files)

    print(f"\n🎉 All pages rendered to '{OUTPUT_DIR}/' including sitemap and homepage!")


if __name__ == "__main__":
    main()
