const stateHandle = document.querySelector("select#id_state");
const tabForms = document.querySelectorAll("div.tab");
const susForms = document.querySelectorAll("div.sus");
const injForms = document.querySelectorAll("div.inj");

const stateFormsList = [tabForms, susForms, injForms]
const stateForms = {
    "Tab": tabForms,
    "Suspension": susForms,
    "Injectable": injForms
}

function updateForm() {
    const state = stateHandle.value;
    stateFormsList.forEach((forms) => {
        forms.forEach((form) => {
            form.classList.add("hidden");
        });
    });

    stateForms[state].forEach((form) => {
        form.classList.remove("hidden");
        const formInput = form.getElementsByTagName("input")[0];
        formInput.setAttribute("required", true);
    });
}

stateHandle.addEventListener("change", (e) => {
    updateForm();
});

document.onload = updateForm();