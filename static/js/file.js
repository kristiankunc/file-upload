function generateFile(file) {
	file = file[0];
	filenameDiv = document.getElementById("filename");
	metadataDiv = document.getElementById("metadata");

	filenameDiv.innerHTML = file.filename;
	metadataDiv.innerHTML = `Custom name: ${file.custom_name}, Size: ${humanFileSize(file.size)}, uploaded at ${file.uploaded_at}`;
}
