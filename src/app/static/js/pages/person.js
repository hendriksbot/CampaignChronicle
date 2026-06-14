const socket = io();

socket.emit("request_person", {
  id: PERSON_ID,
});

socket.on("updated_person", (person) => {
  if (person.id === PERSON_ID) {
    document.getElementById("person-container").innerHTML = person.markdown_rendered;
  }
});
