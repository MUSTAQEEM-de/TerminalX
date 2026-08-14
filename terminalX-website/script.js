/* =========================================
   TERMINALX
   JavaScript
========================================= */


/* =========================================
   MOBILE MENU
========================================= */

const mobileMenu = document.getElementById("mobileMenu");
const navLinks = document.getElementById("navLinks");

if (mobileMenu) {
    mobileMenu.addEventListener("click", () => {

        navLinks.classList.toggle("mobile-open");

        if (navLinks.classList.contains("mobile-open")) {
            navLinks.style.display = "flex";
            navLinks.style.position = "absolute";
            navLinks.style.top = "74px";
            navLinks.style.left = "0";
            navLinks.style.right = "0";
            navLinks.style.flexDirection = "column";
            navLinks.style.padding = "25px";
            navLinks.style.background = "#15292E";
            navLinks.style.borderBottom = "1px solid rgba(255,255,255,0.08)";
        } else {
            navLinks.style.display = "";
        }

    });
}


/* =========================================
   HERO TERMINAL ANIMATION
========================================= */

const typingText = document.getElementById("typingText");
const terminalResponse = document.getElementById("terminalResponse");

const heroCommands = [
    {
        command: "install git",
        response: `
            <div class="terminal-output">Understanding request...</div>
            <div class="terminal-output muted">Detected OS: Ubuntu</div>
            <div class="terminal-output">Action: install_package</div>
            <div class="terminal-output">Risk: DANGEROUS</div>
            <div class="terminal-output">Privilege: SUDO REQUIRED</div>
            <br>
            <div class="terminal-output">Proceed? [y/N] y</div>
            <div class="terminal-output">Installing Git...</div>
            <div style="color:#1DA27E;">✓ Git installed successfully</div>
            <div style="color:#1DA27E;">✓ Installation verified</div>
        `
    },

    {
        command: "show my RAM usage",
        response: `
            <div class="terminal-output">Understanding request...</div>
            <div class="terminal-output muted">Detected OS: Ubuntu</div>
            <div class="terminal-output">Action: show_ram_usage</div>
            <div class="terminal-output">Risk: SAFE</div>
            <br>
            <div style="color:#1DA27E;">RAM Usage: 6.4 GB / 16 GB</div>
            <div style="color:#1DA27E;">✓ Completed</div>
        `
    },

    {
        command: "create a folder called projects",
        response: `
            <div class="terminal-output">Understanding request...</div>
            <div class="terminal-output">Action: create_folder</div>
            <div class="terminal-output">Path: ~/projects</div>
            <div class="terminal-output">Risk: MODERATE</div>
            <br>
            <div class="terminal-output">Proceed? [y/N] y</div>
            <div style="color:#1DA27E;">✓ Folder created</div>
            <div style="color:#1DA27E;">✓ Verified</div>
        `
    }
];


let currentCommand = 0;


function typeHeroCommand() {

    if (!typingText || !terminalResponse) {
        return;
    }

    const item = heroCommands[currentCommand];

    typingText.textContent = "";
    terminalResponse.innerHTML = "";

    let index = 0;

    const typingInterval = setInterval(() => {

        typingText.textContent += item.command[index];

        index++;

        if (index >= item.command.length) {

            clearInterval(typingInterval);

            setTimeout(() => {

                terminalResponse.innerHTML = item.response;

                setTimeout(() => {

                    currentCommand =
                        (currentCommand + 1) % heroCommands.length;

                    typeHeroCommand();

                }, 4200);

            }, 600);
        }

    }, 55);
}


setTimeout(typeHeroCommand, 1000);


/* =========================================
   INTERACTIVE DEMO
========================================= */

const demoButtons =
    document.querySelectorAll(".demo-prompt");

const demoOutput =
    document.getElementById("demoOutput");


const demoData = {

    ram: {
        request: "show my RAM usage",

        content: `
            <div>
                <span class="prompt">TerminalX &gt;</span>
                show my RAM usage
            </div>

            <br>

            <div style="color:#1C8585;">
                Understanding request...
            </div>

            <div style="color:#789B99;">
                Action: show_ram_usage
            </div>

            <div style="color:#789B99;">
                Risk: SAFE
            </div>

            <br>

            <div style="color:#1DA27E;">
                RAM Usage: 6.4 GB / 16 GB
            </div>

            <div style="color:#1DA27E;">
                ✓ Verified
            </div>
        `
    },


    folder: {

        content: `
            <div>
                <span class="prompt">TerminalX &gt;</span>
                create a folder called projects
            </div>

            <br>

            <div style="color:#1C8585;">
                Action: create_folder
            </div>

            <div style="color:#789B99;">
                Path: ~/projects
            </div>

            <div style="color:#789B99;">
                Risk: MODERATE
            </div>

            <br>

            <div style="color:#1DA27E;">
                Proceed? [y/N] y
            </div>

            <div style="color:#1DA27E;">
                ✓ Folder created
            </div>

            <div style="color:#1DA27E;">
                ✓ Verified
            </div>
        `
    },


    git: {

        content: `
            <div>
                <span class="prompt">TerminalX &gt;</span>
                install git
            </div>

            <br>

            <div style="color:#1C8585;">
                Action: install_package
            </div>

            <div style="color:#789B99;">
                Package: git
            </div>

            <div style="color:#789B99;">
                Risk: DANGEROUS
            </div>

            <div style="color:#789B99;">
                Privilege: SUDO REQUIRED
            </div>

            <br>

            <div style="color:#1DA27E;">
                Proceed? [yes/no] yes
            </div>

            <div style="color:#789B99;">
                Installing Git...
            </div>

            <div style="color:#1DA27E;">
                ✓ Git installed successfully
            </div>

            <div style="color:#1DA27E;">
                ✓ Installation verified
            </div>
        `
    },


    nginx: {

        content: `
            <div>
                <span class="prompt">TerminalX &gt;</span>
                restart nginx
            </div>

            <br>

            <div style="color:#1C8585;">
                Action: service_control
            </div>

            <div style="color:#789B99;">
                Service: nginx
            </div>

            <div style="color:#789B99;">
                Operation: restart
            </div>

            <div style="color:#789B99;">
                Risk: DANGEROUS
            </div>

            <br>

            <div style="color:#1DA27E;">
                Proceed? [yes/no] yes
            </div>

            <div style="color:#789B99;">
                Restarting nginx...
            </div>

            <div style="color:#1DA27E;">
                ✓ Service restarted
            </div>

            <div style="color:#1DA27E;">
                ✓ Service verified active
            </div>
        `
    },


    blocked: {

        content: `
            <div>
                <span class="prompt">TerminalX &gt;</span>
                delete everything
            </div>

            <br>

            <div style="color:#1C8585;">
                Analyzing request...
            </div>

            <div style="color:#C98D8D;">
                Potentially destructive operation
            </div>

            <br>

            <div style="
                border:1px solid rgba(180,90,90,.35);
                padding:15px;
                border-radius:6px;
                color:#D99A9A;
            ">
                <strong>✕ OPERATION BLOCKED</strong>

                <br><br>

                This request represents a potentially
                destructive system-wide operation.

                <br><br>

                No changes were made.
            </div>
        `
    }

};


function showDemo(name) {

    const data = demoData[name];

    if (!data || !demoOutput) {
        return;
    }

    demoOutput.style.opacity = "0";

    setTimeout(() => {

        demoOutput.innerHTML = data.content;

        demoOutput.style.transition = "opacity .3s ease";

        demoOutput.style.opacity = "1";

    }, 180);

}


demoButtons.forEach(button => {

    button.addEventListener("click", () => {

        demoButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        showDemo(button.dataset.demo);

    });

});


showDemo("ram");


/* =========================================
   SCROLL REVEAL
========================================= */

const revealElements =
    document.querySelectorAll(
        ".feature-card, .flow-step, .comparison-card, .command-row, .tech-item"
    );


const revealObserver =
    new IntersectionObserver(
        (entries, observer) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add("reveal");

                    observer.unobserve(entry.target);

                }

            });

        },
        {
            threshold: 0.12
        }
    );


revealElements.forEach(element => {
    revealObserver.observe(element);
});


/* =========================================
   SMOOTH CLOSE MOBILE NAV
========================================= */

document.querySelectorAll(".nav-links a").forEach(link => {

    link.addEventListener("click", () => {

        if (window.innerWidth <= 1000) {
            navLinks.style.display = "";
            navLinks.classList.remove("mobile-open");
        }

    });

});