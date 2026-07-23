$(document).ready(function () {

var stripePublicKey =$('#id_stripe_public_key').text().slice(1,-1);
var clientSecret = $('#id_client_secret').text().slice(1,-1);
var fullName = $('#id_full_name').text().slice(1,-1);
var email = $('#id_email').text().slice(1,-1);
var phone = $('#id_phone').text().slice(1,-1);
        
var bStreetAddress1 = $('#id_billing_street_address1');
var bStreetAddress2 = $('#id_billing_street_address2');
var bTown = $('#id_billing_town'); 
var bCounty = $('#id_billing_county'); 
var bCountry = $('#id_billing_country'); 
var bPostcode = $('#id_billing_postcode'); 

var sStreetAddress1 = $('#id_shipping_street_address1');
var sStreetAddress2 = $('#id_shipping_street_address2');
var sTown = $('#id_shipping_town'); 
var sCounty = $('#id_shipping_county'); 
var sCountry = $('#id_shipping_country'); 
var sPostcode = $('#id_shipping_postcode');

var stripe = Stripe(stripePublicKey);

const appearance = {
  theme: 'flat',
  inputs: 'spaced',
  labels: 'floating',
  variables: {
    fontFamily: ' "Montserrat Alternates", sans-serif',
    fontSizeBase:'16px',
    fontLineHeight: '1.5',
    borderRadius: '20px',
    colorBackground: '#FFF',
    colorText:'#2c0f06',
    colorPrimary:'#990099',
    iconColor:'#990099',
    colorDanger:'#b44145',
    colorWarning:'#b44145',
    colorSuccess:'#448848',
    accessibleColorOnColorPrimary: '#2c0f06',
    labelFontSize:'12px',
    focusBoxShadow:'0 0 0 0.25rem #e9e7de',
    inputColorBorder:'#2c0f06',
  },
};

var style ={
    base: {
        color: '#2c0f06',
        fontFamily: '"Montserrat Alternates", sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#2c0f0677'
        }
    },
    invalid: {
        color: '#b44145',
        iconColor: '#b44145'
    }
};

// Enable the skeleton loader UI for the optimal loading experience.
const loader = 'auto';

// Create an elements group from the Stripe instance, passing the clientSecret (obtained in step 2), loader, and appearance (optional).
const elements = stripe.elements({clientSecret, appearance, loader});

// Create Element instances
const paymentElement = elements.create('card', {style:style}, );

// Mount the Elements to their corresponding DOM node
paymentElement.mount("#card-element");

// Handle realtime errors from card element
paymentElement.addEventListener('change',function(event){
    var errorDiv = document.getElementById('card-errors');

    if (event.error){
        var html =`
            <span class="icon" roles="alert">
                <i class="fa-solid fa-triangle-exclamation"></i>
            </span>
            <span>${event.error.message}</span>`
        $(errorDiv).html(html); 
        }
    else{
        $(errorDiv).textContent = '';
    }
});

var gifting = document.getElementById('gifting-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    paymentElement.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#gifting-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    var saveInfo = Boolean($('#id_save_details').attr('checked'));
    
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
        'is_gift' : $trim(gifting.is_gift.value),
        'gift_message':$trim(gifting.gift_message),
    };
    var url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function() {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: fullName,
                    phone: phone,
                    email: email,
                    address: {
                        line1: bStreetAddress1,
                        line2: bStreetAddress2,
                        city: bTown,
                        country: bCountry,
                        state: bCounty,
                    }
                }
            },
            shipping:{
                name: fullName,
                phone: phone,
                address: {
                    line1: sStreetAddress1,
                    line2: sStreetAddress2,
                    city: sTown,
                    country: sCountry,
                    postal_code: sPostcode,
                    state: sCounty,
                }
            }
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                paymentElement.update({ 'disabled': false});
                $('#gifting-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        //just reload the page, the error will be in the django messages
        location.reload();
    })

});



});