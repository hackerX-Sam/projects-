document.addEventListener("DOMContentLoaded", () => {
  function analyzePassword() {
      const pwd = document.getElementById("password").value;
      const bar = document.getElementById("bar");
      const feedback = document.getElementById("feedback");
    
      let strength = 0;
      let message = [];
    
      if (pwd.length >= 8) strength++;
      else message.push("Minimum 8 characters");
    
      if (/[A-Z]/.test(pwd)) strength++;
      else message.push("Add uppercase letters");
    
      if (/[a-z]/.test(pwd)) strength++;
      else message.push("Add lowercase letters");
    
      if (/[0-9]/.test(pwd)) strength++;
      else message.push("Include numbers");
    
      if (/[^A-Za-z0-9]/.test(pwd)) strength++;
      else message.push("Use special characters");
    
      const colors = ["#ef4444", "#f97316", "#facc15", "#10b981", "#22c55e"];
      const widths = ["20%", "40%", "60%", "80%", "100%"];
      const labels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"];
    
      bar.style.width = widths[strength - 1] || "0%";
      bar.style.background = colors[strength - 1] || "gray";
      feedback.innerText = pwd.length === 0 ? "" :
        strength === 5 ? "Perfect password!" : `${labels[strength - 1]}: ${message.join(", ")}`;
    }
});
