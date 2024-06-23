document.addEventListener("DOMContentLoaded", (event) => {
	let comments = document.querySelectorAll("[id^=comment-]");

	comments.forEach((comment) => {
		let commentId = comment.id.split("-")[1];
		let commentText = comment.querySelector("td").innerText;

		fetch("/predict", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ comment: commentText }),
		})
			.then((response) => response.json())
			.then((data) => {
				let sentimentText;
				let color;
				switch (data.sentiment) {
					case 0:
						sentimentText = "Neutral 😑";
						color = "table-primary";
						break;
					case 1:
						sentimentText = "Positive 😊";
						color = "table-success";
						break;
					case 2:
						sentimentText = "Negative 😔";
						color = "table-danger";
						break;
					default:
						sentimentText = "Error";
						color = "table-warning";
				}
				comment.querySelector(
					"td:nth-child(2)"
				).innerText = `${data.sentiment} - ${sentimentText}`;
				console.log(
					comment.querySelector("td:nth-child(2)").parentElement
						.classList
				);
				comment
					.querySelector("td:nth-child(2)")
					.parentElement.classList.add(color);
			})
			.catch((error) => {
				console.error("Error:", error);
				comment.querySelector("td:nth-child(2)").innerText = "Error";
			});
	});
});
