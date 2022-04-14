from customer.models import Profile
from django.urls import reverse

def profile_html_render(user_profile,gender_option_html):
    with open("/home/shihab2004/Chaldal/dynamicStaric/profile.css.js.txt") as f:
        loading = f.read().replace("{{is_geo}}","true"if user_profile.is_geoLocation()else "false").replace("{{POST_API}}",reverse("customer:post_data"))



    secendary_script = """
        <script>

                                                $('#profile_photo').mouseenter((e)=>{

                                                    $('#profile_photo').append(`
                                                    <div class='profile_photoss ana' style=' position: absolute; top:${e.offsetY}px ;left: ${e.offsetX}px;'>
                                                        <div style="display: flex;justify-content: center;height:100%;align-items: center;flex-direction: column;">
                                                            <i style='color:red;font-size:18px' class="fas fa-camera"></i>
                                                            <span style="font-weight: 500;font-size:14px;">Upload Photo</span>
                                                        </div>

                                                    <div>
                                                    `)
                                                })

                                                $('#profile_photo').mouseleave((e)=>{

                                                   $('.profile_photoss div').remove()
                                                   $('.profile_photoss').removeClass('ana');
                                                   $('.profile_photoss').addClass('bana');
                                                   $('.profile_photoss').css('left',5);
                                                   $('.profile_photoss').css('top',5);
                                                   setTimeout(()=>{
                                                    $('.profile_photoss').remove()
                                                   },400)

                                                })

                                                $('#profile_photo').click(()=>{
                                                    const file =$('#profle_file').click();
                                                })

                                                $('#profle_file').change(()=>{
                                                    const file = $('input#profle_file')[0].files[0]
                                                    const url = URL.createObjectURL(file)
                                                    $('#dp_profile').css('background-image',`url(${url})`)

                                                    $('body').append(`

                                                    <div class="cancelContainer ordCM">

                                                        <div class="ModalDialogContainer orderCancelPrompt">
                                                        <div class="ModalDialog">
                                                            <div class="ModalDialogContent">
                                                            <div>
                                                                <div class="modal-text">
                                                                <h1>Are you sure?</h1>
                                                                <p>You want to change your current profile photo?</p>
                                                                </div>
                                                                <div class="modal-footer">
                                                                <button class="btnSecondary">Yes</button>
                                                                <button class="btnPrimary">No</button>
                                                                </div>
                                                            </div>
                                                            </div>
                                                        </div>
                                                        </div>
                                                    </div>
                                                `)

                                                    $('.ordCM .btnPrimary').click(()=>{
                                                        $('.ordCM').remove()
                                                        $('#dp_profile').css('background-image',`url({{profile.profile_photo.url}})`)
                                                    })
                                                    $('.ordCM .btnSecondary').click(()=>{
                                                        $('.ordCM').remove();
                                                        const profile_form = new FormData();
                                                        profile_form.append('csrfmiddlewaretoken',csrfmiddlewaretoken);
                                                        profile_form.append('profile_photo',file)
                                                        $.ajax({
                                                            type:"POST",
                                                            url:"{% url 'customer:post_data2' %}?update_profile=True",
                                                            enctype: "multipart/form-data",
                                                            cache: false,
                                                            processData: false,
                                                            contentType: false,
                                                            data:profile_form,
                                                            success:(data)=>{
                                                                console.log(data);
                                                            }

                                                        })
                                                    })


                                                })
                                            </script>
    """
    profile_pppp =  user_profile.profile_photo.url if user_profile.profile_photo else None
    secendary_script = secendary_script.replace('{{profile.profile_photo.url}}',profile_pppp) if profile_pppp else secendary_script
    secendary_script = secendary_script.replace("{% url 'customer:post_data2' %}",reverse("customer:post_data2"))
    is_email_test = '<span class="input-extra-content" style="margin-top: -11px;"><div class="extraContentForEmail"><button class="btn btn-danger emailVerify verifyBtn">VERIFY</button></div></span>' if not user_profile.user.email else ""
    lol_js = ""
    if is_email_test:
        lol_js = """
                                            <script>
                                            $('.emailVerify').click((e)=>{
                                                e.preventDefault();
                                                const emailVal = $('input[name="email"]').val();
                                                const is_match = emailVal.match(/\w+@\w+\.\D+/);
                                                if(is_match){
                                                    $.ajax({
                                                    method:"POST",
                                                    url:"/customer/api/post2/?email_varify=True",
                                                    data:{
                                                        'email':emailVal,
                                                        'csrfmiddlewaretoken':csrfmiddlewaretoken
                                                    }
                                                    })
                                                }else{
                                                    console.log(e.currentTarget.closest('.inputContainer'));
                                                    e.currentTarget.closest('.inputContainer').querySelector('.input-error').style.display = "block";
                                                    e.currentTarget.closest('.inputContainer').querySelector('.input-error').textContent = "Your Email is Invalid🙂"
                                                }
                                                console.log("sdad");
                                            })


                                           </script>
        """
    allu_js = """
                                         <script>
                                                if($('input[name="email"]').val()){
                                                    $('input[name="email"]').parent().find('.input-placeholder').addClass('aluoooos')
                                                }

                                                $('input[name="email"]').change((e)=>{
                                                if(e.currentTarget.value){
                                                    e.currentTarget.closest('.inputContainer').querySelector('.input-placeholder').classList.add('aluoooos');
                                                }else{
                                                    e.currentTarget.closest('.inputContainer').querySelector('.input-placeholder').classList.remove('aluoooos');

                                                }
                                            })
                                            </script>
    """
    html = f"""


                <section class="bodyTable">
                    <div class="profile">
                        <h2 class="profile-title">Your Profile</h2>
                        <div class="profile-info">
                            <form>
                                <div class="inputContainer">
                                    <div id="profile_photo" class="profile_photo">
                                        <div id="dp_profile" style="background-image: url({profile_pppp})"></div>
                                    </div>

                                    <input id="profle_file" type="file">
                                    {secendary_script}


                                </div>
                                <div class="inputContainer">
                                    <input class="has-value" name="user-name" type="text" required maxlength="70" value="{user_profile.user.username}">
                                    <span class="input-placeholder">Name</span>
                                    <span class="input-error"></span>
                                    <span class="input-extra-content"></span>
                                </div>
                                <div class="inputContainer">
                                    <input class="paddingForExtraContent" name="email" type="email" value="{user_profile.user.email}">
                                    <span class="input-placeholder">Email Address</span>
                                    <span class="input-error"></span>
                                    {allu_js}
                                    {is_email_test}
                                </div>

                                {lol_js}
                                <div class="inputContainer disable">
                                    <input class="has-value" name="number" type="text" disabled value="+880{user_profile.Phone}">
                                    <span class="input-placeholder">Phone Number</span>
                                    <span class="input-error"></span>
                                    <span class="input-extra-content">
                                </div>

                                <div class="inputContainer" data-reactid=".26j8ymn200w.6.2.0.0.1.0.3">
                                    <label class="labelClass" data-reactid=".26j8ymn200w.6.2.0.0.1.0.3.0">Gender</label>
                                    <select name="gender" class="selectClass">
                                        {gender_option_html}
                                    </select>
                                </div>
                            </form>
                        </div>

                         {loading}
                        <section id="adress_choise_show">

                        </section>


                        </div>
                </section>
                    <script>setTitle('{user_profile.user}')</script>
            """
    return html


def adressHtml(profile):
    adress_list_html = ""
    for count ,adress in enumerate(profile.get_all_adress()):
        adress_list_html += f"""
                            <section class="addresses">
                                <div class="address disableAddressSelection" data-address="1682035">
                                    <span class="selectedAddressTickIcon">
                                        <svg style="fill:#3BB07E;stroke:#3BB07E;display:inline-block;vertical-align:middle;" width="20px" height="20px" version="1.1" viewBox="0 0 100 100" x="0px" y="0px">
                                            <path d="M50,88.6c21.3,0,38.6-17.3,38.6-38.6S71.3,11.4,50,11.4S11.4,28.7,11.4,50S28.7,88.6,50,88.6z M31.8,45.9l12.3,12.3  l22.5-22.5l3,3L44.1,64.2L28.8,48.9L31.8,45.9z"></path>
                                        </svg>
                                    </span>
                                    <span>
                                        <p>{adress.adress}</p>
                                        <span class="addressArea"><span class="l-Adress">{adress.area.name}</span>, {adress.city.Name}</span>
                                    </span>
                                    <a pk="{adress.pk}" name="{adress.delivery_parson_name}" area="{adress.area.pk}" adress="{adress.adress}" phone="{adress.Phone}" adress_add="false" id="edit_adress_modals_{count}" targetId="target_modals_{count}" onclick="modals_render(this)">Edit</a>
                                </div>

                                <div id="target_modals_{count}">

                                </div>
                            </section>
        """
    area_option_html = ""
    for area in profile.current_city.get_area.all():
        area_option_html += f"<option value='{area.pk}'>{area.name}</option>"
    print(area_option_html)
    with open("/home/shihab2004/Chaldal/dynamicStaric/adress.js.txt") as f:
       js = f.read()
       js = js.replace("{{current_city}}",profile.current_city.Name)
       js = js.replace("{{area_option_html}}",area_option_html)
       js = js.replace("{% url 'customer:post_data' %}",reverse("customer:post_data"))
    html = f"""
            <div style="max-width:600px" class="address-block checkoutExperience2">
                <div class="deliveryStep activeStep">
                    <div class="deliveryStepTitle">
                        <div class="titleLeft">
                            <h2>Address Book</h2>
                        </div>
                    </div>
                    <div class="deliveryStepContent">
                        <div class="addressComponent mui">
                            <div class="">
                                <section class="">
                                    <div id="update_adress" pk="0" name="{profile.user.username}" adress="" phone="{profile.Phone}" adress_add="true" targetId="update_adress_modals" onclick="modals_render(this)" class="newAddressAddBtn buttonOnTop">
                                        <section>
                                            <svg width="15px" height="15px" style="display:inline-block;vertical-align:middle;" version="1.1" viewBox="5 7 22 22" x="0px" y="0px">
                                                <g stroke-width="1">
                                                    <rect height="19" width="1" x="16" y="7"></rect>
                                                    <rect height="1" width="19" x="7" y="16"></rect>
                                                </g>
                                            </svg>
                                            <span>New Address</span>
                                        </section>
                                    </div>
                                    <div id="update_adress_modals"></div>



                                                        {js}

                                                                <section id="localAdress-list">

                                                                    {adress_list_html}

                                                                </section>

                                </section>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    """

    return html

from root.models import City

def selectCityHtml(profile):
    city_html = ""
    user_profile_city_pk = profile.current_city.pk if profile else None
    for count , city in enumerate(City.objects.all()):
        current_city =  "isSelected" if user_profile_city_pk  == city.pk else ""
        city_html += f"<div id='{city.pk}' class='cityChoice {current_city}'><div class='cityImageContainer'><img src='{city.get_image()}' class='cityImage'></div><div class='cityName'><p>{city.Name}</p></div></div>"

    js = """
      <script>
        $(".cityChoice").click((e)=>{
            $(".cityChoice").removeClass("isSelected")
            e.currentTarget.classList.add("isSelected")
            const city_id = e.currentTarget.id
            $.ajax({
                method:"POST",
                data:{
                    "current_city":city_id,
                    'csrfmiddlewaretoken': csrfmiddlewaretoken,
                },
                url:"[[post_data2]]?update_current_city=True",
                success:(sucData)=>{
                    console.log(sucData);
                    if(sucData.state == "successful"){
                        $(".metropolitanAreaName").text(sucData.city);
                        sessionStorage.setItem("select_city_html","");
                        $('.citySelectionInlineLink .cityName').text(sucData.city);
                    }
                }
            })
        })
        setTitle('City')
    </script>
    """
    js = js.replace("[[post_data2]]",reverse("customer:post_data2"))
    html = f"""
        <section class="bodyTableasd">
            <div>
                <div class="citySelectionPage">
                    <div class="content-wrapper">
                        <h1>Select City</h1>
                        <div class="cityOptions">
                            {city_html}
                        </div>
                    </div>
                </div>
            </div>
        </section>
    {js}

    """

    return html