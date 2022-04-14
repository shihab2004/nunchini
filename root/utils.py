from django.shortcuts import redirect


def image_or_link(image,link):
        if not image:
            return link
        return image.url


def slugify(char):
    ccr=  """[@_!#$%^&*;()<>?/\|}{~:]"'"""
    c1 = char.lower()
    c2 = c1.split(" ")
    value = ""
    k=0
    for i in c2:
        if k < len(c2)-1:
            k+=1   
            if i in ccr:
                        continue
            value += f"{i}_"

        else:
                  value += f"{i}"
        
    return value


def almost_same(root,menu):
    main_menu =  menu.objects.filter(parent=None)
    return {
        "root":root,
        "main_menu":main_menu
    }

def super_user_required(func):
    def check(request,*args, **kwargs):
        if request.user.is_superuser:
            return func(request,*args, **kwargs)
        else:return redirect('/')
    return check



from re import split
def get_svg_text_form_file(file):
    
    if file:
        text = split(r"<svg",file.read().decode())
        return "<svg"+text[1]
    return ""
