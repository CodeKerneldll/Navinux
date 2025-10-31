
---

### **3️⃣ autoreload.md**

```markdown
# Extensão Auto Refresh
Recarrega a página a cada 30 segundos

```python
from PyQt6.QtCore import QTimer

timer = QTimer()
timer.timeout.connect(lambda: browser.reload())
timer.start(30000)  # 30 segundos
