"""
This snippet searches Deezer for new albums that were issued by your favorite
artists, arranges their covers in a nice table and sends the html by mail
Please configure this program by putting a configuration yaml in ~/.deezer_mails
with the following content:

config:
  address: example@yahoo.com
  smtp_server: smtp.mail.yahoo.com
  port: 587
  run_every_days: 7
  deezer_id: 1234567891
"""

from collections import defaultdict
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
from math import ceil
import smtplib
import time
import os
import yaml
from string import Formatter

from deezer_python.deezer import Deezer


def load_config(path="~/.deezer_mails"):
    return yaml.load(open(os.path.expanduser(path)))


def send_html_as_mail(html, address, password, smtp_server, port=587):
    subject = "Your new releases for " + datetime.datetime.now().strftime('%d.%m.%Y')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = address
    msg['To'] = address

    text = "Cannot display HTML!"
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(address, password)
        server.sendmail(address, address, msg.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit() 


def get_released_albums(artists, since_dt):
    released_albums = []
    for artist in artists:
        albums = artist.get_all_albums()
        for album in albums:
            release_date = datetime.datetime.strptime(album.release_date, '%Y-%m-%d')
            if release_date > since_dt:
                released_albums.append(album)

    return released_albums


def album_cover_art(albums, albums_per_row=4):
    """ Creates a table of all the album covers in HTML """
    # Create HTML code with placeholders for the individual cells
    html_table = ''
    rows = int(ceil(len(albums) / albums_per_row))
    for i in range(rows):
        cells = "".join(['{cell' + str(i*albums_per_row + a) + '} '
                         for a in range(albums_per_row)])
        html_table += '<tr>\n' + cells + '</tr>\n'


    # Create a dict with the HTML code for the individual cells
    cell_html_dict = defaultdict(lambda: '')

    for i, album in enumerate(albums):
        album.reload_all_fields()

        description = u"{} - {}".format(album.artist.name, album.title)\
            .encode('ascii', 'ignore')

        cell_html = """<td><a href="{album_url}">
        <img src="{cover_link}" title="{description}" alt="{description}"
        style="width:100%;height:100%;"></a> </td>\n"""

        cell_html = cell_html.format(album_url=album.link,
                                     cover_link=album.cover_big,
                                     description=description)
        cell_html_dict['cell' + str(i)] = cell_html


    # Format the cells into the table
    html = '<table cellspacing="0" cellpadding="0" style="width:100%">\n'
    fmt = Formatter()
    html += fmt.vformat(html_table, (), cell_html_dict)
    html += '</table>'

    return html


def read_last_run_time():
    try:
        with open('last_search_time.txt', 'r') as f:
            return datetime.datetime.strptime(f.readline().strip(),
                                              '%Y-%m-%d')
    except IOError:
        print("Defaulting to beginning of year")
        return datetime.datetime.now().replace(month=1, day=1)


def write_last_run_time():
    with open('last_search_time.txt', 'w') as mfile:
        mfile.write(datetime.datetime.now().strftime('%Y-%m-%d'))


if __name__ == '__main__':
    config = load_config()['config']
    print("Please type your email pwd here:")
    email_pass = getpass()

    deezer = Deezer(config['deezer_id'])

    while True:
        search_time = read_last_run_time()
        artists = deezer.get_favorite_artists()
        released_albums = get_released_albums(artists, search_time)

        print("{} new albums were released..".format(len(released_albums)))
        html = album_cover_art(released_albums)

        print("Sending message")
        send_html_as_mail(html, config['address'], email_pass,
                          config['smtp_server'], config['port'])
        print("Done!")

        write_last_run_time()

        print("Will now sleep..")
        time.sleep(60 * 60 * 24 * int(config['run_every_days']))
