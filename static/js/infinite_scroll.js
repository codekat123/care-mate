document.addEventListener("DOMContentLoaded", () => {
  const list = document.getElementById("list-object");
  const loadMore = document.getElementById("load-more");
  const nextLink = document.getElementById("next-link");
  if (!list || !loadMore || !nextLink) return;

  let loading = false;

  const observer = new IntersectionObserver(async (entries) => {
    if (!entries[0].isIntersecting || loading) return;

    loading = true;
    const url = nextLink.getAttribute("href");

    try {
      const res = await fetch(url);
      const text = await res.text();

      // Parse response
      const parser = new DOMParser();
      const doc = parser.parseFromString(text, "text/html");

      // Grab new items
      const newItems = doc.querySelectorAll("#doctor-list .doctor-card");
      newItems.forEach(item => list.appendChild(item));

      // Update next page link
      const newNext = doc.querySelector("#next-link");
      if (newNext) {
        nextLink.setAttribute("href", newNext.getAttribute("href"));
      } else {
        loadMore.innerHTML = "<p class='text-muted'>No more results</p>";
        observer.unobserve(loadMore);
      }
    } catch (err) {
      console.error("Infinite scroll error:", err);
    } finally {
      loading = false;
    }
  }, { rootMargin: "300px" });

  observer.observe(loadMore);
});
