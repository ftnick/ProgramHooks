window.onload = function() {
    // Array of plugin objects with title, description, link, and date
    const pluginList = [
        {
            title: "Internal Plugin",
            description: "Handles some internal functionality.",
            link: "https://raw.githubusercontent.com/ftnick/ProgramHooks/refs/heads/main/plugins/_internal.py",
            date: "October 9th, 2024"
        },
        {
            title: "Example Plugin",
            description: "Prints notices when certain stages are executed.",
            link: "https://raw.githubusercontent.com/ftnick/ProgramHooks/refs/heads/main/plugins/Example.py",
            date: "October 9th, 2024"
        }
    ];

    const pluginSection = document.getElementById('plugin-list');

    // Dynamically populate the plugin list
    if (pluginList.length > 0) {
        pluginList.forEach(plugin => {
            // Create list item for each plugin
            const li = document.createElement('li');

            // Plugin title as a clickable link
            const title = document.createElement('a');
            title.href = plugin.link;
            title.textContent = plugin.title;
            title.target = "_blank";  // Open the link in a new tab
            title.style.fontWeight = 'bold';
            li.appendChild(title);

            // Line break for separation
            li.appendChild(document.createElement('br'));

            // Description
            const desc = document.createElement('p');
            desc.textContent = plugin.description;
            li.appendChild(desc);

            // Date uploaded
            const date = document.createElement('p');
            date.textContent = `Uploaded on: ${plugin.date}`;
            date.style.fontStyle = 'italic';
            li.appendChild(date);

            // Add the plugin item to the plugin list
            pluginSection.appendChild(li);
        });
    } else {
        const status = document.getElementById('plugin-status');
        status.textContent = 'No plugins available at the moment.';
    }
};
