# Intro

This is a recon-ng script that will parse a given users instagram account and pull down all of the images/videos from that account

# usage
drop this script into the **modules/recon/profiles-profiles** directory

```
[recon-ng][default] > use recon/profiles-profiles/instagram
[recon-ng][default][instagram] > show options

  Name      Current Value  Required  Description
  --------  -------------  --------  -----------
  USERNAME  blah           yes       Username of person

[recon-ng][default][instagram] > set username mohdid
USERNAME => mohdid
[recon-ng][default][instagram] > run
[*] Account is legit, lets start parsing Instagram
[*] 25 image(s) identified, downloading now...
[recon-ng][default][instagram] > 

```

By default the script will dump everything into your **workspace/instagram/** directory
