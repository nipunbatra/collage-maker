// Simple, elegant lightbox for gallery images
class SimpleLightbox {
    constructor() {
        this.currentIndex = 0;
        this.images = [];
        this.init();
    }

    init() {
        // Get all gallery images
        this.images = Array.from(document.querySelectorAll('.gallery-image'));
        
        // Add click handlers
        this.images.forEach((img, index) => {
            img.style.cursor = 'pointer';
            img.addEventListener('click', (e) => {
                e.preventDefault();
                this.open(index);
            });
        });

        // Create lightbox HTML
        this.createLightbox();
        
        // Add keyboard support
        document.addEventListener('keydown', (e) => {
            if (this.isOpen) {
                switch(e.key) {
                    case 'Escape':
                        this.close();
                        break;
                    case 'ArrowLeft':
                        this.prev();
                        break;
                    case 'ArrowRight':
                        this.next();
                        break;
                }
            }
        });
    }

    createLightbox() {
        const lightbox = document.createElement('div');
        lightbox.id = 'lightbox';
        lightbox.innerHTML = `
            <div class="lightbox-overlay">
                <div class="lightbox-container">
                    <button class="lightbox-close">&times;</button>
                    <button class="lightbox-prev">&#8249;</button>
                    <button class="lightbox-next">&#8250;</button>
                    <div class="lightbox-content">
                        <img class="lightbox-image" src="" alt="">
                        <div class="lightbox-info">
                            <h3 class="lightbox-title"></h3>
                            <p class="lightbox-caption"></p>
                            <div class="lightbox-counter"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(lightbox);
        
        // Add event listeners
        lightbox.querySelector('.lightbox-close').addEventListener('click', () => this.close());
        lightbox.querySelector('.lightbox-prev').addEventListener('click', () => this.prev());
        lightbox.querySelector('.lightbox-next').addEventListener('click', () => this.next());
        lightbox.querySelector('.lightbox-overlay').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) this.close();
        });
        
        this.lightboxElement = lightbox;
        this.lightboxImage = lightbox.querySelector('.lightbox-image');
        this.lightboxTitle = lightbox.querySelector('.lightbox-title');
        this.lightboxCaption = lightbox.querySelector('.lightbox-caption');
        this.lightboxCounter = lightbox.querySelector('.lightbox-counter');
        this.isOpen = false;
    }

    open(index) {
        this.currentIndex = index;
        this.updateContent();
        this.lightboxElement.style.display = 'block';
        document.body.style.overflow = 'hidden';
        this.isOpen = true;
        
        // Fade in animation
        setTimeout(() => {
            this.lightboxElement.querySelector('.lightbox-overlay').style.opacity = '1';
        }, 10);
    }

    close() {
        this.lightboxElement.querySelector('.lightbox-overlay').style.opacity = '0';
        setTimeout(() => {
            this.lightboxElement.style.display = 'none';
            document.body.style.overflow = 'auto';
            this.isOpen = false;
        }, 300);
    }

    prev() {
        this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
        this.updateContent();
    }

    next() {
        this.currentIndex = (this.currentIndex + 1) % this.images.length;
        this.updateContent();
    }

    updateContent() {
        const img = this.images[this.currentIndex];
        this.lightboxImage.src = img.src;
        this.lightboxImage.alt = img.alt;
        this.lightboxTitle.textContent = img.dataset.title || img.alt;
        this.lightboxCaption.textContent = img.dataset.caption || '';
        this.lightboxCounter.textContent = `${this.currentIndex + 1} of ${this.images.length}`;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SimpleLightbox();
});