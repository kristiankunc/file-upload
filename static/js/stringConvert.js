function formatString(fileString) {
	const fileArray = fileString.replaceAll("&#39;", '"').replaceAll("None", null).split("}, {");

	fileArray[0] = fileArray[0].replaceAll("[{", "{");
	fileArray[fileArray.length - 1] = fileArray[fileArray.length - 1].replaceAll("}]", "}");

	console.log(fileArray);
	for (let i = 0; i < fileArray.length; i++) {
		fileArray[i] = fileArray[i].replaceAll("{", "").replaceAll("}", "").replaceAll("'", '"');

		fileArray[i] = "{" + fileArray[i] + "}";

		fileArray[i] = JSON.parse(fileArray[i]);

		fileArray[i].uploaded_at = new Date(fileArray[i].uploaded_at * 1000).toLocaleString("cs-CZ", { timeZone: "Europe/Prague" });
	}

	return fileArray;
}

function humanFileSize(bytes, si = false, dp = 1) {
	const thresh = si ? 1000 : 1024;

	if (Math.abs(bytes) < thresh) {
		return bytes + " B";
	}

	const units = si ? ["kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"] : ["KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"];
	let u = -1;
	const r = 10 ** dp;

	do {
		bytes /= thresh;
		++u;
	} while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);

	return bytes.toFixed(dp) + " " + units[u];
}
