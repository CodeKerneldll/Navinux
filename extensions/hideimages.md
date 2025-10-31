
---

### **8️⃣ hideimages.md**

```markdown
# Extensão Hide Images
Oculta todas as imagens da página

```python
js_code = """
let imgs = document.querySelectorAll('img');
for(let img of imgs){ img.style.display='none'; }
"""
browser.page().runJavaScript(js_code)
