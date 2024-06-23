let fb_pages_container = document.querySelector("#fb_pages_container");
let posts_container = document.querySelector("#posts_container");

const fetchPages = () => {
	// GET ALL PAGES NAME WITH FETCH REQUEST
	fetch(`${window.location.origin}/get-pages`, {
		method: "POST",
	})
		.then((response) => response.json())
		.then((res) => {
			fb_pages_container.innerHTML = "";
			if (res.data) {
				for (let i = 0; i < Object.keys(res.data).length; i++) {
					const currentPage = res.data[i];
					const page_template = `
                        <a href="${window.location.origin}/page/${currentPage.id}/posts/" class="btn btn-primary px-4 me-3">${currentPage.name}</a>
                        `;
					fb_pages_container.innerHTML += page_template;
				}
			}
		});
};

// WHEN ALL THE DOM ELEMENT LOADED
document.addEventListener("DOMContentLoaded", () => {
	// FETCH ALL THE FACEBOOK PAGES OF THE USER
	fetchPages();
});
