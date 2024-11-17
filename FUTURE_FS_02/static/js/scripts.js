const products = [
    { id: 1, name: "Silk Scarf", price: 2000, description: "Light and luxurious." },
    { id: 2, name: "Elegant Blouse", price: 3000, description: "Perfect for any occasion." }
  ];
  const cart = [];
  
  function displayProducts() {
    const productSection = document.getElementById("products");
    products.forEach(product => {
      const productElement = document.createElement("div");
      productElement.innerHTML = `
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <p>Price: Ksh ${product.price}</p>
        <button onclick="addToCart(${product.id})">Add to Cart</button>
      `;
      productSection.appendChild(productElement);
    });
  }
  
  function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    cart.push(product);
    alert(`${product.name} has been added to the cart.`);
  }
  displayProducts();
  