function generateFiles(files) {
	const table = document.getElementById("files-table");

	files.forEach((file) => {
		const row = document.createElement("tr");
		row.innerHTML = `
            <td>${file.id}</td>
            <td>${file.filename}</td>
            <td>${humanFileSize(file.size)}</td>
            <td>${file.custom_name}</td>
            <td>${file.uploaded_at}</td>
        `;
		table.appendChild(row);
	});
}
