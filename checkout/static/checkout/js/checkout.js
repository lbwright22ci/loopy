var stripePublicKey =$('#id_stripe_public_key').text().slice(1,-1);
var clientSecret = $('#id_client_secret').text().slice(1,-1);

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

// Enable the skeleton loader UI for the optimal loading experience.
const loader = 'auto';

// Create an elements group from the Stripe instance, passing the clientSecret (obtained in step 2), loader, and appearance (optional).
const elements = stripe.elements({clientSecret, appearance, loader});

// Create Element instances

// Passing in defaultValues is optional, but useful if you want to prefill consumer information to
// ease consumer experience.
const paymentElement = elements.create('card', {
  defaultValues: {
    billingDetails: {
      name: 'John Doe',
      phone: '888-888-8888',
    },
  },
});

// Mount the Elements to their corresponding DOM node

paymentElement.mount("#card-element");