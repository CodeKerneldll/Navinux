
---

### **6️⃣ customcss.md**

```markdown
# Extensão Custom CSS
Injeta CSS customizado na página

```python
css = """
body { font-family: Arial, sans-serif !important; line-height: 1.5; }
a { color: #ff6f61 !important; }
"""
js_code = f"""
let style = document.createElement('style');
style.innerHTML = `{css}`;
document.head.appendChild(style);
"""
browser.page().runJavaScript(js_code)
