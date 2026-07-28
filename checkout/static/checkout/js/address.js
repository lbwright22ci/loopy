// This sample uses the Places Autocomplete widget to:
// 1. Help the user select a place
// 2. Retrieve the address components associated with that place
// 3. Populate the form fields with those address components.
// This sample requires the Places library, Maps JavaScript API.

// code from Google Maps Platform

let placeAutocomplete;
let address1Field;
let address2Field;
let postalField;

async function init() {
    await google.maps.importLibrary('places');

    placeAutocomplete = document.querySelector('gmp-place-autocomplete');
    address1Field = document.querySelector('#id_billing_street_address1');
    address2Field = document.querySelector('#id_billing_street_address2');
    postalField = document.querySelector('#id_billing_postcode');
    

    // Handle user selection on the autocomplete widget.
    placeAutocomplete.addEventListener('gmp-select', ({ placePrediction }) => {
        void fillInAddress(placePrediction);
    });

}

async function fillInAddress(placePrediction) {
    // The placePrediction object does not have all the details needed
    // for the form, so we'll call fetchFields to get the place details.
    const place = placePrediction.toPlace();
    await place.fetchFields({ fields: ['addressComponents'] });

    let address1 = '';
    let postcode = '';

    if (!place.addressComponents) {
        return;
    }

    // Populate form fields with address component data.
    // The field is only updated if the types array includes
    // the specified type-value.

    for (const component of place.addressComponents) {
        
        if (component.types.includes('street_address')) {
            address1 = `${component.longText} ${address1}`;
        }

        if (component.types.includes('street_number')) {
            address1 = `${component.longText} ${address1}`;
        }

        if (component.types.includes('route')) {
            address1 += component.shortText;
        }

        if (component.types.includes('postal_code')) {
            postcode = `${component.longText}${postcode}`;
        }

        if (component.types.includes('postal_town')) {
            document.querySelector('#id_billing_town').value = component.longText;
        }

        if (component.types.includes('administrative_area_level_2')) {
            document.querySelector('#id_billing_county').value = component.shortText;
        }

        if (component.types.includes('country')) {
            document.querySelector('#id_billing_country').value = component.longText;
        }
    }

    address2Field.value = "";
    postalField.value = postcode;
    address1Field.value = address1;

    // After filling the form with address components from the Autocomplete
    // prediction, set cursor focus on the second address line to encourage
    // entry of subpremise information such as apartment, unit, or floor number.
    address2Field.focus();
}

void init();