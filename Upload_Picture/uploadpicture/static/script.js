document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById('fireworks');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    class Firework {
        constructor(x, y, color) {
            this.x = x;
            this.y = y;
            this.color = color;
            this.particles = [];
            this.createParticles();
        }

        createParticles() {
            for (let i = 0; i < 50; i++) {
                this.particles.push({
                    x: this.x,
                    y: this.y,
                    angle: Math.random() * Math.PI * 2,
                    speed: Math.random() * 4 + 2,
                    size: Math.random() * 3 + 1,
                    alpha: 1
                });
            }
        }

        update() {
            this.particles.forEach(p => {
                p.x += Math.cos(p.angle) * p.speed;
                p.y += Math.sin(p.angle) * p.speed;
                p.alpha -= 0.02;
            });
            this.particles = this.particles.filter(p => p.alpha > 0);
        }

        draw() {
            this.particles.forEach(p => {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(${this.color.r}, ${this.color.g}, ${this.color.b}, ${p.alpha})`;
                ctx.fill();
            });
        }
    }

    let fireworks = [];

    function createFirework(x, y) {
        const color = { r: Math.random() * 255, g: Math.random() * 255, b: Math.random() * 255 };
        fireworks.push(new Firework(x, y, color));
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        fireworks.forEach(f => f.update());
        fireworks.forEach(f => f.draw());
        fireworks = fireworks.filter(f => f.particles.length > 0);
        requestAnimationFrame(animate);
    }

    setInterval(() => createFirework(Math.random() * canvas.width, Math.random() * (canvas.height / 2)), 700);
    animate();

    // ==============================
    // XEM TRƯỚC ẢNH KHI CHỌN FILE
    // ==============================
    document.querySelector("input[type='file']").addEventListener("change", function (event) {
        let file = event.target.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = function (e) {
                document.getElementById("preview").src = e.target.result;
                document.getElementById("preview-container").style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });

    // ==============================
    // UPLOAD ẢNH & HIỂN THỊ KẾT QUẢ
    // ==============================
    
});

