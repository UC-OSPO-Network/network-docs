SLIDES      := iassist-2026-slides
SLIDES_FULL := iassist-2026-slides-full
PORT        := 4848
PORT_FULL   := 4849
PDF_TITLE   := "Open Source as Institutional Infrastructure"

.PHONY: all html pdf pptx full full-html full-pdf full-pptx clean

all: html pdf pptx

html:
	quarto render $(SLIDES).qmd --to revealjs

pdf: html
	@python3 -m http.server $(PORT) --directory . &
	@sleep 3
	decktape reveal http://localhost:$(PORT)/$(SLIDES).html $(SLIDES).pdf \
		--size 1280x720 --pdf-title $(PDF_TITLE)
	@pkill -f "http.server $(PORT)" 2>/dev/null || true

pptx:
	quarto render $(SLIDES).qmd --to pptx

# Full (19-slide) deck
full: full-html full-pdf full-pptx

full-html:
	quarto render $(SLIDES_FULL).qmd --to revealjs

full-pdf: full-html
	@python3 -m http.server $(PORT_FULL) --directory . &
	@sleep 3
	decktape reveal http://localhost:$(PORT_FULL)/$(SLIDES_FULL).html $(SLIDES_FULL).pdf \
		--size 1280x720 --pdf-title $(PDF_TITLE)
	@pkill -f "http.server $(PORT_FULL)" 2>/dev/null || true

full-pptx:
	quarto render $(SLIDES_FULL).qmd --to pptx

clean:
	rm -f $(SLIDES).pdf $(SLIDES).pptx $(SLIDES_FULL).pdf $(SLIDES_FULL).pptx
