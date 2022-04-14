from customer.models import user_adress



def get_adress(profile,id=None,):
    try:
        adress = profile.adress.get(pk=id)
        return adress
    except (user_adress.DoesNotExist,ValueError):
        return None
