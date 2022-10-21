      // A reference to Stripe.js initialized with a fake API key.
const stripe = Stripe("pk_test_51KoRoySBDBtenKQMAkZDxxqFW8VOXo43Hjfx6PDzGDW5X75ftYErlFaCltn1B8RIKkg7pxHaGHlCVsGPCNZwuNpZ006Q6ndqik");

// The items the customer wants to buy
const items = [{ id: "xl-tshirt" }];
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

let elements;

initialize();
checkStatus();

document
  .querySelector("#payment-form")
  .addEventListener("submit", handleSubmit);


// Fetches a payment intent and captures the client secret
async function initialize() {
  const response = await fetch("create-checkout-session/", {
    method: "POST",
    headers: { "Content-Type": "application/json", 
    // 'Accept': 'application/json',         
    'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ items }),
  });
  const { clientSecret } = await response.json();

  const appearance = {
    theme: 'stripe',
  };
  elements = stripe.elements({ appearance, clientSecret });

  const paymentElement = elements.create("payment");
  paymentElement.mount("#payment-element");
}

async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);
  console.log("adads");
  const type=document.querySelector('.inf').dataset.val;
  const id=document.querySelector('.inf').dataset.id;
  console.log(document.querySelector('.inf').dataset)
  console.log(type)
  console.log(id)
  const url="http://localhost:8000/success"

  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      // Make sure to change this to your payment completion page
      return_url: "http://localhost:8000/success/"+`${id}`+"/"+`${type}`,
      // return_url: "{% url 'success' %}",
    },
  });

  // This point will only be reached if there is an immediate error when
  // confirming the payment. Otherwise, your customer will be redirected to
  // your `return_url`. For some payment methods like iDEAL, your customer will
  // be redirected to an intermediate site first to authorize the payment, then
  // redirected to the `return_url`.
  if (error.type === "card_error" || error.type === "validation_error") {
    console.log("bbbb");
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occured.");
    console.log("sfsf");

  }

  setLoading(false);
}

// Fetches the payment intent status after payment submission
async function checkStatus() {
  const clientSecret = new URLSearchParams(window.location.search).get(
    "payment_intent_client_secret"
  );
  console.log(clientSecret);
  if (!clientSecret) {
    return;
  }

  const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

  switch (paymentIntent.status) {
    case "succeeded":
      showMessage("Payment succeeded!");
      break;
    case "processing":
      showMessage("Your payment is processing.");
      break;
    case "requires_payment_method":
      showMessage("Your payment was not successful, please try again.");
      break;
    default:
      showMessage("Something went wrong.");
      break;
  }
}

// ------- UI helpers -------

function showMessage(messageText) {
  const messageContainer = document.querySelector("#payment-message");

  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;

  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageText.textContent = "";
  }, 4000);
}

// Show a spinner on payment submission
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}
      
      