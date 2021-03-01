import pipedrive as pi

p = pi.remove_dupe_website()

for i in range (len(p)):
    id_one = p['Organization - ID'][i]
    id_opt = p['Merge Id'][i]
    if id_one == id_opt:
        pass
    elif id_one != id_opt :
        pi.merge_orga(id_one,id_opt)