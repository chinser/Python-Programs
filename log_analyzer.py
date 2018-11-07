#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';
import gzip
import os.path
import re

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}

def parse_line(line):
  parse_path = re.compile(r"""
  ^
  # ---------------$remote_addr:
  (?P<remote_addr>
  \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}
  )
  \ {1,}
  # ---------------$remote_user:
  (?P<remote_user>
    [a-zа-яёЁ_\-\[\]\\^{}|`]
    [a-zа-яёЁ0-9\-\[\]\\^{}|`]*
  )
  \ {1,}
  # ---------------$http_x_real_ip:
  (?P<http_x_real_ip>
    \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\-
  )
  \ {1,}
  # ---------------[$time_local]:
  (?P<time_local>
    \[[\s\S]+\]
  )
  \ {1,}
  # ---------------"$request"
  (?P<request>
    \"[\s\S]+\"
  )
  \ {1,}
  # ---------------'$status:
  (?P<status>
    \d+
  )
  \ {1,}
  # ---------------$body_bytes_sent:
  (?P<body_bytes_sent>
    \d+
  )
  \ {1,}
  # ---------------"$http_referer" '
  (?P<http_referer>
    \"[\s\S]+\"
  )
  \ {1,}
  # ---------------'"$http_user_agent"
  (?P<http_user_agent>
    \"[\s\S]+\"
  )
  \ {1,}
  # ---------------"$http_x_forwarded_for"
  (?P<http_x_forwarded_for>
    \"[\s\S]+\"
  )
  \ {1,}
  # ---------------"$http_X_REQUEST_ID"
  (?P<http_X_REQUEST_ID>
    \"[\s\S]+\"
  )
  \ {1,}
  # ---------------"$http_X_RB_USER" '
  (?P<http_X_RB_USER>
    \"[\s\S]+\"
  )
  \ {1,}
  # ---------------'$request_time'
  (?P<request_time>
    \d+\.\d+
  )$
  """, re.VERBOSE | re.UNICODE | re.IGNORECASE)

  #text = u":ник-с-кириллицей-и-Ё!~ident@host PRIVMSG #channel : test message"
  #line = u'1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390'
  #1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390
  #1.99.174.176 3b81f63526fa8  - [29/Jun/2017:03:50:22 +0300] "GET /api/1/photogenic_banners/list/?server_name=WIN7RB4 HTTP/1.1" 200 12 "-" "Python-urllib/2.7" "-" "1498697422-32900793-4708-9752770" "-" 0.133
  #1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/16852664 HTTP/1.1" 200 19415 "-" "Slotovod" "-" "1498697422-2118016444-4708-9752769" "712e90144abee9" 0.199
  #1.199.4.96 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/slot/4705/groups HTTP/1.1" 200 2613 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-3800516057-4708-9752745" "2a828197ae235b0b3cb" 0.704
  #1.168.65.96 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/internal/banner/24294027/info HTTP/1.1" 200 407 "-" "-" "-" "1498697422-2539198130-4709-9928846" "89f7f1be37d" 0.146
  #1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/group/1769230/banners HTTP/1.1" 200 1020 "-" "Configovod" "-" "1498697422-2118016444-4708-9752747" "712e90144abee9" 0.628
  #1.194.135.240 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/group/7786679/statistic/sites/?date_type=day&date_from=2017-06-28&date_to=2017-06-28 HTTP/1.1" 200 22 "-" "python-requests/2.13.0" "-" "1498697422-3979856266-4708-9752772" "8a7741a54297568b" 0.067
  #1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/1717161 HTTP/1.1" 200 2116 "-" "Slotovod" "-" "1498697422-2118016444-4708-9752771" "712e90144abee9" 0.138
  #1.166.85.48 -  - [29/Jun/2017:03:50:22 +0300] "GET /export/appinstall_raw/2017-06-29/ HTTP/1.0" 200 28358 "-" "Mozilla/5.0 (Windows; U; Windows NT 6.0; ru; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729)" "-" "-" "-" 0.003

  match = parse_path.match(line)

  return match
  #if match:
  #  print([item for item in match.groups()])


def main():
     LOG_DIR = config.get("LOG_DIR")
     URL_dict = {} #словарь URL
     #nginx-access-ui.log-20170630.gz 
     namedatestr = re.compile(r'\d{4}\d{2}\d{2}.gz|\d{4}\d{2}\d{2}.log')
     datestr = re.compile(r'\d{4}\d{2}\d{2}')
     names = [name for name in os.listdir(LOG_DIR) if os.path.isfile(os.path.join(LOG_DIR, name)) and namedatestr.findall(name)]
     maxdatestr = '20010101'
     maxfilename = ''
     for name in names:
         datename = datestr.findall(name)[0]
         if datename > maxdatestr:
           maxfilename = name
           maxdatestr = datename

     if maxfilename != '':
        filename = LOG_DIR + '/' + maxfilename
        if maxfilename.find('.gz') != -1:
            #f = gzip.open(filename, 'rt') # for line in f: print(line) break выдает ошибку UnicodeDecodeError
            URL_all_count = 0
            URL_all_time_sum = 0
            with gzip.open(filename, 'rt') as f:
              for line in f:
                URL_all_count += 1
                matched = parse_line(line)
                if matched:
                    URL_all_time_sum += float(matched.group(13))
                    URL = matched.group(5)
                    fromURL = URL_dict.get(URL)
                    if fromURL != None: #урл уже есть в словаре
                      URL_count = fromURL.get('count') #получим количество урлов
                      URL_count += 1
                      URL_count_perc = URL_count / URL_all_count * 100 #получим % от общего числа запросов для этого урл
                      URL_time_sum = fromURL.get('time_sum') #получим суммарный request_time для данного урл
                      URL_time_max = max(fromURL.get('time_max'), float(matched.group(13)) )
                      URL_time_sum += float(matched.group(13))
                    else: # урл встречается первый раз
                      URL_count = 1
                      URL_count_perc = 1 / URL_all_count * 100
                      URL_time_sum = float(matched.group(13))
                      URL_time_max = URL_time_sum

                    if URL_all_time_sum == 0:
                      URL_time_perc = 0
                    else:
                      URL_time_perc = URL_time_sum / URL_all_time_sum * 100
                    URL_time_avg = URL_time_sum / URL_count
                    URL_dict.update({URL: {"count": URL_count, "count_perc": URL_count_perc, "time_sum": URL_time_sum,
                                           "time_perc": URL_time_perc, "time_avg": URL_time_avg, "time_max": URL_time_max,
                                           "time_med": URL_time_med}})
                if URL_all_count == 3:
                  break

        #if maxfilename.find('.log') != -1:
        #    f = open(filename, 'rt')
        
        #with f as f1:
         #   for line in f1:
          #    #print(line)
           #   break

# or match.group('nickname'), match.group('identifier'), etc

#'1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390'

# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';
        

     pass
    #f = gzip.open

if __name__ == "__main__":
    main()
