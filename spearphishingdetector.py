# -*- coding: utf-8 -*-
"""SpearPhishingDetector.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J4Z2rdwJHJMwBttY3Utey2WXHNK6VZV1

**Anticipation des statégies d'hameçonnage par email par les techniques de IA(ML, DL et NLP)**
"""

'''
Bibliotheques Python nécessaire et configuration initiale

'''

#  Libreries python nécessaire
from colorama import Fore, Back, Style
import colorama
form colorama import Fore, Style,Back
colorama.init()
import re, os, sys
from bs4 import BeautifulSoup
import pprint
from urlparse import urlparse
import email
from IPy import IP
import email.header
import csv
from collections import Counter
from pandas as pd
from sklearn.externals import joblib


# Definition de l'encodage à l'UTF-8 et imprimer la sortie sur Jupiter Notebook

stdout = sys.stdout
reloard(sys)
sys.setdefaultencoding('UTF8')
sys.stdout = stdout

'''
Fonction de pré-traitement supplémentaires

'''

print(Fore.MAGENTA)
print(Back.YELLOW)
print(30 * "*" + "SpearPhishingDetector" + 30 * "*")
print(Style.RESET_ALL)

test_path = input(Fore.BLUE + "Entrez le chemin du dossier où se trouve le courrier : ")


# Difference entre deux listes

def difference(first, second):
  second = set(second)
  for item in first:
    first.remove(item)
  return first

# Compte le nombre de caractere dans une chaine donnée

def count_characters(string):
  return len(string) - string.count(' ') - string.count('\n')

# Extrait une URL dans le corps du message

def extract_urls(msg):
  mail = str(msg)
  urls = re.findall(r"http[s]?://(?://([a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", mail)
  return urls

# Extraire les urls d'encrage dans le message

def extract_achor_urls(msg):
  anchor_urls =[]
  soup = BeautifulSoup(msg, 'html.parser')
  for link in soup.findAll('a', attrs={'href': re.compile("^http[s]?://")}):
    anchor_urls.append(link.get('href'))
  return anchor_urls

# Extraire le domaine de l'émail

def get_email_domain(strings):
  domain = re.search("@[\w.]+", string)
  if domain is None:
    return None
  return str(domaine.group())[1:]

# Extraine le domaine de l'url

def get_url_domain(url):
  domain = None
  if url:
    if u'@' in str(url):
      domain = get_email_domain(str(url))
    else:
      parsed_uri = urlparse(url)
      domain = '{uri.netloc}'.format(uri=parsed_uri)
      if domain.startwith("www."):
        return domain[4:]
  return domain


# Trouver l'url la pus frequente dans une liste d'URLs

def most_common_url(urls):
  if urls:
    modal_url = max(set(urls), key = urls.count)
    return modal_url
    else:
      return None

# Supprimer le fichier s'il existe

def remove_if_exists(filename):
  try:
    os.remove(filename):
    except OSError:
      pass

'''
Functions needed to extract the necessary fields

'''
# Get paths to spam, test, easy_ham, phishing_2015 and phishing_2016 folders
#spam_path = "C:/Users/FENNY/Desktop/ML-Case Study/spamassasin/New folder/OWN/dataset/spam"
#test_path = "C:/Users/FENNY/Desktop/BE-Final/SPAM-ASSA/dataset/"
#ham_path = "C:/Users/FENNY/Desktop/ML-Case Study/spamassasin/New folder/OWN/dataset/easy_ham"
#phishing_2015_path = "C:/Users/FENNY/Desktop/ML-Case Study/spamassasin/New folder/OWN/dataset/mbox/phishing_2015"
#phishing_2016_path = "C:/Users/FENNY/Desktop/ML-Case Study/spamassasin/New folder/OWN/dataset/mbox/phishing_2016"


# Lire les fichiers (nom de fichiers) dans le chemin choisi

def get_files(path):
  mail_files(path):
  mail_files = os.listdir(path)
  return mail_files

# Extraire le message de l'email(lu commeune chaine)

def extract_msg(path, mail_file):
  mail_file = path + '/' + mail_file
  fh = open(mail_file, "rb")
  mail = fp.read()
  fp.close()

  msg = email.message_from_string(mail)
  return msg

# Extraire le corps du message

def extract_body(msg):
  body_content = ""
  if msg.is_multipart():
    for payloard in msg.get_payloard():
    body_content += str(payloard.get_payloard())
  else:
    body_content += msg.get_payloard()
  return body_content

# Extraire le sujet du message

def extract_subj(msg):
  decode_subj = email.header(msg['Subject'])[0]
  try:
    suj_content = unicode(decode_subj[0])
  except:
    subj_content = "None"
  return subj_content

# Extraire l'adresse de l'expéditeur du méssage

def extract_send_address(msg):
  decode_send = email.header(msg['From'])[0]
  try:
    send_adress = unicode(decode_send[O])
  except:
      send_address = "None"
  return send_address

# Extraire l'url modale du message

def extract_modal_url(msg):
  urls = extract_urls(msg)
  modal_url = most_common_url(urls)
  return modal_url

# Extraire tous les liens

def extract_all_links(msg):
  links = []
  soup = BeautifulSoup(msg, 'html.parser')
  for link in soup.finAll('a'):
    links.append(link.get('href'))

  all_urls = extract_urls(msg)
  anchor_urls = extract_anchor_urls(msg)

  urls = difference(all_urls, anchor_urls)
  links = links = urls
  return links

  '''

  Extraction des champs nécessaires

  '''

# Exécutez la fonction pour extraire les champs nécessaires d'un dossier

def extract_necessary_fields(path, mail):
  necessary_fields = {}
  msg = extract_msg(path, mail):
  necessary_fields = {}
  msg = extract_msg(path, mail)

  necessary_fields['body'] = extract_body(msg)
  necessary_fields['subj'] = extract_subj(msg)
  necessary_fields['send'] = extract_send_address(msg)
  necessary_fields['replyTo'] = extract_replyTo_address(msg)
  necessary_fields['modalURL'] = extract_modal_url(msg)
  necessary_fields['links'] = extract_all_links(msg)

  return necessary_fields


#  Verifions que tous ce qui a été faite jusqu'ici est coorrecte

'''
Fonctions our extraire les attributs basés sur le corps

'''

# Booléen : si le code HTML est présent ou pas

def body_html(body_content):
  body_html = bool(BeautifulSoup(body_content, "html.parser").find("form"))
  return body_forms

# Entier : nombre de mot dans le corps

def body_noWords(body_content):
  body_noWords = len(body_content.split())
  return body_noWords

# Entier : nombre de caractere dans le corps

def body_noCharacters(body_content):
  body_noCharacters = count_characters(body_content)
  return body_noCharacters

# Entier : Nombre de mots distints dans le corps du texte

def body_noDistinctWords(body_content):
  body_noDistinctWords = len(Counter(body_content.split()))
  return body_noDistinctWords

# Flottant : richesse du texte(corps)

def body_richness(body_noWords, body_noCharacters):
  try:
    body_richness = float(body_noWords)/body_noCharacters
  except:
    body_richness = 0
  return body_richness

# Entier : Nombre de mots de fonction dans le corps

def body_noFunctionWords(body_content):
  body_noFunctionWords = 0
  wordList = re.sub("^A-Za-z", "", body_content.strip()).lower().split()
  function_words = ["account", "access", "bank","credit", "click", "identity", "inconvenience", "information", "limited", "log", "minutes", "password", "recently", "risk", "social", "security", "service", "suspended"]
  for word in function_words:
    body_noFunctionWords += wordlist.count(word)
  return body_noFunctionWords

# Booléen : Si le corps contient ou non le mot "suspenssion"

def body_suspension(body_content):
  body_suspension = "suspension" in body_content.lower()
  return body_suspension

# Booléen : si le corps contient ou non la phrase "verifier votre compte"

def body_verifyYourAccount(body_content):
  phrase = "verifyyouraccount"
  content = re.sub(r"[^A-Za-z]", "", body_content.strip()).lower()
  body_verifyYourAccount = phrase in content
  return body_verifyYourAccount

def extract_body_attributes(body_content):
  body_attributes = {}

  body_attributes['body_html'] = body_html(body_content)
  body_attributes['body_forms'] = body_forms(body_content)
  body_attributes['body_noWords'] = body_html(body_content)
  body_attributes['body_html'] = body_noWords(body_content)
  body_attributes['body_noCharacters'] = body_noCharacters(body_content)
  body_attributes['body_richness'] = body_html(body_attributes['body_noWords'], body_attributes['body_noCharacters'])
  body_attributes['body_noFunctionWords'] = body_noFunctionWords(body_content)
  body_attributes['body_suspension'] = body_suspension(body_content)
  body_attributes['body_verifyYourAccount'] = body_verifyYourAccount(body_content)

  return body_attributes

  '''
Fonctions d'extraction des attributs de la ligne d'objet

'''

# Booléen : Verifier si le courrier est une reponse a un courrier precendent

def subj_reply(subj_content):
  subj_reply = subj_content.lower().startswith("re:")
  return subj_reply

# Bouleen : vérifier si le courrier est une redurection d'un autre courriel

def subj_forward(subj_content):
  subj_forward = subj_content.lower().startswith("fwd:")
  return subj_forward

# Entier : nombre de mot dans le sujet

def subj_noWords(subj_content):
  subj_noWords = len(subj_content.split())
  return subj_noWords

# Entier : nombre de caracteres dans le sujet

def subj_noCharacters(subj_content):
  subj_noCharacters = count_characters(subj_content)
  return subj_noCharacters

# Flottant : richesse du texte (sujet)

def subj_richness(subj_noWords, subj_noCharacters):
  try:
    subj_richness = float(subj_noWords)/subj_noCharacters
  except:
    subj_richness = 0
  return subj_richness

# Booleen : Si le sujet contient le mot "vérifier" ou non

def subj_verify(subj_content):
  subj_verify = "verify" in subj_content.lower()
  return subj_verify

# Booleen : si le sujet contient ou non le mot "debit"

def subj_debit(subj_content):
  subj_debit = "debit" in subj_content.lower()
  return subj_debit

# Booleen : Si le sujet contient ou non le mot "banque"

def subj_bank(subj_content):
  subj_bank = "bank" in subj_content.lower()
  return subj_bank


def extract_subj_attributes(subj_content):
  subj_attributes(subj_content):
  subj_attributes = {}

  subj_attributes['subj_reply'] = subj_reply(subj_content)
  subj_attributes['subj_forward'] = subj_forward(subj_content)
  subj_attributes['subj_noWords'] = subj_noWords(subj_content)
  subj_attributes['subj_noCharacters'] = subj_noCharacters(subj_content)
  subj_attributes['subj_richness'] = subj_richness(subj_content)
  subj_attributes['subj_verify'] = subj_verify(subj_content)
  subj_attributes['subj_debit'] = subj_debit(subj_content)
  subj_attributes['subj_bank'] = subj_bank(subj_content)

  return subj_attributes



'''
Fonctions d'extraction des attributs basés sur l'adresse de l'expéditeur

'''

# Entier : nombre de mots dans l'adresse de l'expédditeur

def send_noWords(send_address):
  send_noWords = len(send_address.split())
  return send_noWords

# Entier : Nombre de caracteres dans l'adresse de l'expéditeur

def send_noCharacters(send_address):
  send_noCharacters = count_characters(send_address)
  return send_noCharacters

# Booleen : Verifier si les domaines de l'expediteur et du destinataire de la reponse sont different

def send_diffSendReplyTo(send_address, replyTo_address):
  send_diffSendReplyTo = get_email_domain(send_address)
  replyTo_domain = get_email_domain(replyTo_address)

  send_diffSenderReplyTo = False
  if replyTo_address != "None":
    send_diffSenderReplyTo = (send_domain != replyTo_domain)
  return send_diffSenderReplyTo

# Booleen : Verifie si le domaine modal de l'expéditeur et celui de l'email sont differnts

def send_nonModalSenderDomain(send_address, modal_url):
  send_domain = get_email_domain(send_address)
  modal_domain = get_url_domain(modal_url)

  send_nonModalSenderDomain = False
  if str(modal_url) != "None":
    send_nonModalSenderDomain = (send_domain != modal_url)
  return send_nonModalSenderDomain

  def extract_send_attributes(send_address, replyTo_address, modal_url):
    send_attributes = {}

    send_attributes['send_noWords'] = send_noWords(send_address)
    send_attributes['send_noCharacters'] = send_noCharacters(send_address)
    send_attributes['send_diffSenderReplyTo'] = send_diffSenderReplyTo(send_address)
    send_attributes['send_nonModalSenderDomain'] = send_nonModalSenderDomain(send_address)

    return send_attributes

    '''
    Fonctions d'extraction d'attributs basés sur l'URL

    '''

# Bouleen : Si l'on utilse les adress IP plutot que les noms de domaine

def url_iAddress(links_list):
  url_ipAddress = False
  for link in links_list:
    link_address = get_url_domain(link)
    if ":" in str(link_address):
      link_address = link_address[:link_address.index(":")]
    try:
      IP(link_address)
      url_ipAddress = True
      break
    except:
      continue
  return url_ipAddress

# Entier : nombre de liens dans un courriel qui contiennent des address IP

def url_noIpAddresses(links_list):
  url_noIPAddresses = 0
  for link in links_list:
    link_address = get_url_domain(link)
    if ":" in str(link_address):
      link_address = link_address[:link_address.index(":")]
    try:
      IP(link_address)
      url_noIpAddress = url_noIpAddresses + 1
      break
    except:
      continue
  return url_noIpAddresses

# Booleen : Si le symbole "@" est présent dans une url

def url_atSymbol(links_list):
  url_atSymbol = False
  for link in links_url:
    if u'@' in str(link):
      url_atSymbol = True
      break
  return url_atSymbol

# Entier : nombre de liens dans le corps du message

def url_noLinks(links_list):
  url_noLinks = len(links_list)
  return url_noLinks


# Entier : Nombre de liens externes dans le corps du message

def url_noExtLinks(body_content):
  url_noExtLinks = len(extract_urls(body_content))
  return url_noExtLinks

# Entier : Nombre de liens internes dans le corps du message

def url_noIntLinks(lonks_list, body_content):
  url_noIntLinks = url_noLinks(links_list) - url_noExtLinks(body_content)
  return url_noLinks

# Entier : Nombre de kiens vers des images dans le corps du message

def url_noLinks(body_content):
  soup = BeautifulSoup(body_content)
  images_links = soup.finAll('img')
  return len(image_links)

# Entier : Nombre de domaines URL dans le corps du message

def url_noDomains(body_content, send_address, replyTo_address):
  domains = set()
  all_urls = extract_urls(body_content)
  for url in all_urls:
    domain = get_url_domain(url)
    domains.add(get_email_domain(replyTo_address))
    return len(domains)

# Entier : Nombre de périodes dans le lien avec le plus grand nombre de périodes

def url_maxNoPeriods(links_list):
  max_periods = 0
  for link in links_list:
    num_periods = str(link).count('.')
    if max_periodes < num_periods:
      max_periods = num_periods
  return max_periods

# Booleen : vérifier si le texte du lien contient ds termes tels que "cliquer" "ici", "se connecter" ou "mettre à jour".

def url_linkText(body_content):
  url_linkText = False
  linkText = ['click', 'here', 'login', 'update']
  soup = BeautifulSoup(body_content)
  for link in soup.findAll('a'):
    if link.contents:
      contents = list(re.sub(r'([^\s\w]|_)+', '', str(link.contents[0])).lower()split())
      extra_contents = set(contents).difference(set(linkText_words))
      if len(extra_contents) < len(contents):
        url_linkText = True
        break
  return url_linkText

# Booleen: S'il n'existe pas de lien dans le dimain modele  /if 'here' links don't map to modal domain
def url_nonModalHereLinks(body_content, modal_url):
    modal_domain = get_url_domain(modal_url)

    url_nonModalHereLinks = False
    if str(modal_url) != "None":
        soup = BeautifulSoup(body_content)
        for link in soup.findAll('a'):
            if link.contents:
                if "here" in link.contents[0]:
                    link_ref = link.get('href')
                    if get_url_domain(link_ref) != modal_domain:
                        url_nonModalHereLinks = True
                        break
    return url_nonModalHereLinks

# Booleen : Si l'URL accede a un autre port que le port 80
def url_ports(links_list):
    url_ports = False
    for link in links_list:
        link_address = get_url_domain(link)
        if ":" in str(link_address):
            port = link_address[link_address.index(":"):][1:]
            if str(port) != str(80):
                url_ports = True
                break
    return url_ports


# Entier : Nombre de liens avec information sur le port

def url_noPorts(links_list):
    url_noPorts = 0
    for links in link_list:
        link_address = get_url_domain(link)
        if ":" in str(link_address):
            url_noPorts = url_noPorts + 1
    return url_noPorts

def extract_url_attributes(links_list, body_content, send_address, replyTo_address, modal_url):
    url_attributes = {}

    url_attributes['url_ipAddress'] = url_ipAddress(links_list)
    url_attributes['url_noIpAddresses'] = url_noIpAddresses(links_list)
    url_attributes['url_atSymbol'] = url_atSymbol(links_list)
    url_attributes['url_noLinks'] = url_noLinks(links_list)
    url_attributes['url_noExtLinks'] = url_noExtLinks(body_content)
    url_attributes['url_noIntLinks'] = url_noIntLinks(links_list, body_content)
    url_attributes['url_noImgLinks'] = url_noImgLinks(body_content)
    url_attributes['url_noDomains'] = url_noDomains(body_content, send_address, replyTo_address)
    url_attributes['url_maxNoPeriods'] = url_maxNoPeriods(links_list)
    url_attributes['url_linkText'] = url_linkText(body_content)
    url_attributes['url_nonModalHereLinks'] = url_ipAddress(body_content, modal_url)
    url_attributes['url_ports'] = url_ipAddress(links_list)
    url_attributes['url_noPorts'] = url_ipAddress(links_list)

    return url_attributes

'''

FONCTION POUR EXRAIRE LE SCRIPT A BASE DES ATTRIBUTS

'''


# Booleen : si les scripts sont present dans le corps du mail

def script_scripts(body_content):
    script_scripts = bool(BeautifulSoup(body_content, "html.parser").find("script"))
    return script_scripts

# Booleen : Si le script present est en javascript

def script_javaScript(body_content):
    script_javaScript = False
    if script_scripts(body_content):
        soup = BeautifulSoup(body_content)
        for script in soup.findAll('script'):
            if script.get('type') == "text/javascript":
                script_javaScript = True
    return script_javaScript

# Booleen : ooléen : vérifie si le script remplace la barre d'état dans le client de messagerie.

def script_statusChange(body_content):
    script_statusChange = False
    if script_scripts(body_content):
        soup = BeautifulSoup(body_content)
        for script in soup.findAll('script'):
            if "window.status" in str(script.contents):
                script_statusChange = True
    return script_statusChange

# Verifier si le mail contient une fenetre pop-up

def script_popups(body_content):
    script_popups = False
    if script_scripts(body_content):
        soup = BeautifuSoup(body_content)
        for script in soup.findAll('script.contents'):
            if "window.open" in str(script.contents):
                script_popups = True
    return script_popups

# Entier : Nombre d'événements "on-click" (sur le clic)

def scriptnoOnClickEvents(body_content):
    scriptnoOnClickEvents = 0
    if script_scripts(body_content):
        soup = BeautifulSoup(body_content)
        codes = soup.findAll('button',{"onclick":True})
        script_noOnClickEvents = len(codes)
    return script_noOnClickEvents

# Boleen : Si le javascript provient de l'extérieur du domaine modal

def script_nonModalJsLoards(body_content):
  script_nonModalJsLoards = False
if script_scripts(body_content):
    if str(modal_url) != "None":
        soup = BeautifulSoup(body_content)
        for script in soup.findAll('script'):
            source = is not None:
            if get_url_domain(source) != modal_domain:
                    script_nonModalJsLoards = True
                    break
    return script_nonModalJsLoards

def extract_script_attributes(body_content, modal_url):
    script_attributes = {}

    script_attributes['script_scripts'] = script_scripts(body_content)
    script_attributes['script_javaScripts'] = script_javaScripts(body_content)
    script_attributes['script_statusChange'] = script_statusChange(body_content)
    script_attributes['script_popups'] = script_popups(body_content)
    script_attributes['scriptnoOnClickEvents'] = scriptnoOnClickEvents(body_content)
    script_attributes['script_nonModalJsLoards'] = script_nonModalJsLoards(body_content, modal_url)

    return script_attributes
#test_path = "C:/Users/FENNY/Desktop:BE-Final:SPAM-ASSA:dataset/demo/"
mail_files = get_files(test_path)
#print len(mail_files)
#print mail_files[0]
mailOneccessary_fields = extract_neccessary_fieds(test_path, mail_files[0])
#pprint.pprint(mailOneccessary_fields, width = 1)

'''

Overall feature extraction (40 features)

'''

def overall_feature_extraction(path, label, mail):
    necessary_fields = extract_necessary_fields(path, mail)

    body_attributes = extract_body_attributes(necessary_fields['body'])
    subj_attributes = extract_subj_attributes(necessary_fields['subj'])
    send_attributes = extract_send_attributes(necessary_fields['send'], necessary_fields['replyTO'], necessary_fields['modalURL'])
    url_attributes = extract_url_attributes(necessary_fields['links'], necessary_fields['body'], necessary_fields['send'], necessary_fields['replyTO'], necessary_fields['modalURL'])
    script_attributes = extract_script_attributes(necessary_fields['send'], necessary_fields['body'], necessary_fields['modalURL'])


    feautures = body_attributes
    fefeautures.update(subj_attributes)
    fefeautures.update(send_attributes)
    fefeautures.update(url_attributes)
    fefeautures.update(script_attributes)
    feautures['label'] = label

    return feautures

"""# New Section"""