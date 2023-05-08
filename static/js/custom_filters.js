(function () {
  function capitalizeName(name) {
    const articles = ['de', 'da', 'do', 'das', 'dos'];
    const words = name.split(' ');
    const capitalizedWords = words.map(function (word, index) {
      if (index === 0 || articles.indexOf(word.toLowerCase()) === -1) {
        return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
      } else {
        return word.toLowerCase();
      }
    });
    return capitalizedWords.join(' ');
  }

  window.filter = {
    js_capitalize_name: capitalizeName,
  };
})();
