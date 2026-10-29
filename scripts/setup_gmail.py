"""Append missing Gmail placeholders/key locally; never display or replace values."""
from config import ROOT
from gmail_connector.client import generate_key


def main():
    path = ROOT / '.env'
    names = set()
    if path.exists():
        with path.open(encoding='utf-8') as stream:
            for line in stream:
                names.add(line.partition('=')[0].strip())
    defaults = {
        'APPLYSYNC_GOOGLE_CLIENT_ID': 'replace-with-web-client-id.apps.googleusercontent.com',
        'APPLYSYNC_GOOGLE_CLIENT_SECRET': 'replace-with-web-client-secret',
        'APPLYSYNC_GOOGLE_REDIRECT_URI': 'http://127.0.0.1:8000/gmail/callback',
        'APPLYSYNC_GMAIL_FRONTEND_ORIGIN': 'http://127.0.0.1:5173',
    }
    additions = [name+'='+value for name, value in defaults.items() if name not in names]
    if 'APPLYSYNC_GMAIL_ENCRYPTION_KEY' not in names:
        additions.append('APPLYSYNC_GMAIL_ENCRYPTION_KEY='+generate_key())
    if additions:
        with path.open('a', encoding='utf-8') as stream:
            stream.write('\n'+'\n'.join(additions)+'\n')
    print('Missing Gmail settings added locally. Existing values preserved; no secrets displayed.')
    print('Enter the web OAuth client ID and secret in .env locally. Never share the file or key.')


if __name__ == '__main__':
    main()
