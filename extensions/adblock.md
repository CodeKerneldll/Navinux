# Extensão AdBlock

Essa extensão bloqueia URLs de anúncios

```python
from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo
import re

class AdBlockInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info: QWebEngineUrlRequestInfo):
        url = info.requestUrl().toString()
        ad_patterns = [
            r"doubleclick\.net",
            r"ads\.",
            r"googlesyndication",
            r"adservice"
        ]
        if any(re.search(pattern, url) for pattern in ad_patterns):
            info.block(True)

profile = browser.page().profile()
interceptor = AdBlockInterceptor()
profile.setRequestInterceptor(interceptor)
