const onClick = (id) => {
  const cells = document.querySelectorAll(`.cellActive`);
  const titles = document.querySelectorAll(`.cellActive > .cellTitle`);
  const checkboxs = document.querySelectorAll(`.cellActive > .cellCheckbox`);
  for (let i = 0; i < cells.length; i++) {
    cells[i].classList.remove("cellBooked");
    titles[i].innerText = "Có làm việc";
    checkboxs[i].checked = false;
  }

  const cell = document.querySelector(`#${id}`);
  cell.classList.add("cellBooked");
  const title = document.querySelector(`#${id} > .cellTitle`);
  title.innerText = "Đã đặt";
  const checkbox = document.querySelector(`#${id} > .cellCheckbox`);
  checkbox.checked = !checkbox.checked;
};

const navigateToStripe = async (sessionId) => {
  if (sessionId) {
    const stripe = Stripe(
      "pk_test_51QTk0dGERsXi0Zdu1Y6fqeTHHGgwwUMFngdFYr5ayE0VyI2avVQft1yY1H0UW4jR9WM4v1WU5Pj4NumlqN1HjDP000DCdSnfeC",
    );

    const result = await stripe.redirectToCheckout({
      sessionId: sessionId,
    });
  }
};
