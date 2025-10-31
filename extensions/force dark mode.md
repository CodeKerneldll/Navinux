
---

### **2️⃣ darkmode.md**

```markdown
# Extensão Dark Mode

```python
js_code = """
document.body.style.backgroundColor = '#121212';
document.body.style.color = '#e0e0e0';
let elems = document.querySelectorAll('*');
for(let e of elems){ e.style.backgroundColor = '#121212'; e.style.color = '#e0e0e0'; }
"""
browser.page().runJavaScript(js_code)
