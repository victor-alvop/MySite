document.querySelector('.dark-toggle').addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    document.documentElement.setAttribute("data-theme", currentTheme === "dark" ? "light" : "dark");
  });
  
  document.querySelectorAll('nav li[data-target]').forEach(item => {
    item.addEventListener('click', () => {
      const sectionId = item.getAttribute('data-target');
      const section = document.getElementById(sectionId);
      if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
  