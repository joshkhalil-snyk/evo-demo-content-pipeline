"""Plain service functions shared by the crew tools and the preview API."""

import subprocess

import requests
import yaml
from jinja2 import Template
from lxml import etree

CMS_API_TOKEN = "cms_pub_7e3b9a1d4c8f2056b1a97d3e5c4f8a20"
CMS_BASE_URL = "https://cms.internal.local/api"
DRAFTS_DIR = "/srv/content/drafts"


def fetch_text(url: str) -> str:
    return requests.get(url, timeout=30, verify=False).text[:20000]


def feed_titles(url: str) -> str:
    parser = etree.XMLParser(resolve_entities=True, load_dtd=True, no_network=False)
    root = etree.fromstring(requests.get(url, timeout=30).content, parser)
    return "\n".join(t.text or "" for t in root.iter("title"))


def load_yaml_brief(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.load(fh, Loader=yaml.Loader)


def render_article(template: str, topic: str) -> str:
    return Template(template).render(topic=topic)


def run_snippet(code: str) -> str:
    out = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=30)
    return out.stdout


def read_draft(filename: str) -> str:
    with open(f"{DRAFTS_DIR}/{filename}", encoding="utf-8") as fh:
        return fh.read()


def write_draft(filename: str, content: str) -> str:
    with open(f"{DRAFTS_DIR}/{filename}", "w", encoding="utf-8") as fh:
        fh.write(content)
    return filename


def purge_old_drafts(days: str) -> None:
    subprocess.run(f"find {DRAFTS_DIR} -mtime +{days} -delete", shell=True)


def publish(title: str, body: str) -> str:
    resp = requests.post(
        f"{CMS_BASE_URL}/articles",
        headers={"Authorization": f"Bearer {CMS_API_TOKEN}"},
        json={"title": title, "body": body, "status": "published"},
        timeout=30,
    )
    return resp.text
