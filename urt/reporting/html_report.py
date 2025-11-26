import os
from jinja2 import Environment, FileSystemLoader

def save_html_report(results: dict, target: str, out_path: str = None):
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report.html.j2')
    context = {"target": target, "results": results}
    html = template.render(**context)
    path = out_path or os.path.join('reports', target, 'recon.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path
