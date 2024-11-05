const url = 'http://127.0.0.1:8000/core/doc/'

fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(userData => {
    console.log('User Data:', userData);
  })
  .catch(error => {
    console.error('Error:', error);
  });