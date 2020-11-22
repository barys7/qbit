from qbittorrent import Client
def Download(url):
    qb = Client("http://localhost:8080/")
    qb.login("your username","your password")
    qb.download_from_link(url)
