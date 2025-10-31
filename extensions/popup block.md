
---

### **4️⃣ popupblock.md**

```markdown

```python
browser.page().profile().setRequestInterceptor(
    type("PopupBlocker", (), {
        "interceptRequest": lambda self, info: info.block(True)
    })()
)
