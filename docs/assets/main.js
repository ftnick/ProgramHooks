window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const packageType = urlParams.get('package');
    const statusElement = document.getElementById('download-status');

    if (packageType) {
        let downloadLink, fileName;
        if (packageType === 'full') {
            downloadLink = 'assets/downloads/full_package.zip';
            fileName = 'full_package.zip';
            statusElement.textContent = 'Downloaded full example package';
            triggerDownload(downloadLink, fileName);
        } else if (packageType === 'frameworkonly') {
            downloadLink = 'https://raw.githubusercontent.com/ftnick/ProgramHooks/refs/heads/main/hook_manager.py';
            fileName = 'hook_manager.py';
            fetch(downloadLink)
                .then(response => response.text())
                .then(data => {
                    const blob = new Blob([data], { type: 'text/plain' });
                    const url = window.URL.createObjectURL(blob);
                    triggerDownload(url, fileName);
                    window.URL.revokeObjectURL(url);  // Clean up URL object after download
                })
                .catch(error => {
                    statusElement.textContent = 'Error downloading framework package';
                    console.error('Error fetching file:', error);
                });
                statusElement.textContent = 'Downloaded framework file';
        }
    }

    function triggerDownload(url, fileName) {
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;  // Forces the browser to download the file
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
};
