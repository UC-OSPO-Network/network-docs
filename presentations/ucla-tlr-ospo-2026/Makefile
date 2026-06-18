SLIDES    := ucla-tlr-ospo-2026-slides
PORT      := 4850
PDF_TITLE := "Open Source as Institutional Infrastructure"

.PHONY: all html pdf pptx clean

all: html pdf pptx

html:
	quarto render $(SLIDES).qmd --to revealjs

# PDF: render HTML, serve it, export with decktape (Chromium under the hood)
pdf: html
	@python3 -m http.server $(PORT) --directory . >/dev/null 2>&1 &
	@sleep 3
	decktape reveal http://localhost:$(PORT)/$(SLIDES).html $(SLIDES).pdf \
		--size 1280x720 --pdf-title $(PDF_TITLE)
	@pkill -f "http.server $(PORT)" 2>/dev/null || true

pptx:
	quarto render $(SLIDES).qmd --to pptx

clean:
	rm -f $(SLIDES).pdf $(SLIDES).pptx $(SLIDES).html
