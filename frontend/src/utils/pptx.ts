import { Pitch, SlideContent, Claim } from '../types/capabilities';
import { SLIDE_TITLES, PROVENANCE_LABELS } from '../types/contracts';

/**
 * Client-side PPTX exporter using pptxgenjs (dynamically imported inside click handler).
 * Generates a polished 16:9 investor deck.
 */
export async function exportPitchDeckToPptx(
  pitch: Pitch,
  startupName = 'Current Startup'
): Promise<void> {
  const pptxModule = await import('pptxgenjs');
  const PptxGen = pptxModule.default;
  const pres = new PptxGen();

  // 16:9 widescreen layout
  pres.layout = 'LAYOUT_16x9';
  pres.title = `${startupName} - Investor Pitch Deck`;

  // Color palette
  const BG_COLOR = 'F8FAFC'; // slate-50
  const TEXT_PRIMARY = '0F172A'; // slate-900
  const TEXT_SECONDARY = '475569'; // slate-600
  const ACCENT_COLOR = '4F46E5'; // brand indigo-600
  const CARD_BG = 'FFFFFF';

  // Title Slide
  const titleSlide = pres.addSlide();
  titleSlide.background = { color: '0F172A' }; // Dark slate for cover

  titleSlide.addText(startupName, {
    x: 1.0,
    y: 2.2,
    w: 11.3,
    h: 1.2,
    fontSize: 44,
    bold: true,
    color: 'FFFFFF',
    fontFace: 'Arial',
  });

  titleSlide.addText('Investor Pitch Presentation', {
    x: 1.0,
    y: 3.4,
    w: 11.3,
    h: 0.8,
    fontSize: 22,
    color: '818CF8', // Indigo-400
    fontFace: 'Arial',
  });

  titleSlide.addText('Generated & Evaluated by PitchPilot AI Coach', {
    x: 1.0,
    y: 6.2,
    w: 8.0,
    h: 0.5,
    fontSize: 12,
    color: '94A3B8',
    fontFace: 'Arial',
  });

  // 12 Pitch Slides
  pitch.slides.forEach((slide: SlideContent, idx: number) => {
    const s = pres.addSlide();
    s.background = { color: BG_COLOR };

    // Slide Title Header Card
    s.addShape(pres.ShapeType.rect, {
      x: 0.8,
      y: 0.6,
      w: 11.7,
      h: 1.0,
      fill: { color: CARD_BG },
      line: { color: 'E2E8F0', width: 1 },
    });

    s.addText(slide.title || SLIDE_TITLES[slide.key] || `Slide ${idx + 1}`, {
      x: 1.1,
      y: 0.7,
      w: 9.5,
      h: 0.8,
      fontSize: 20,
      bold: true,
      color: TEXT_PRIMARY,
      fontFace: 'Arial',
    });

    s.addText(`SLIDE ${idx + 1} OF 12`, {
      x: 10.5,
      y: 0.7,
      w: 1.8,
      h: 0.8,
      fontSize: 10,
      bold: true,
      color: ACCENT_COLOR,
      fontFace: 'Arial',
      align: 'right',
    });

    // Content Card
    s.addShape(pres.ShapeType.rect, {
      x: 0.8,
      y: 1.8,
      w: 11.7,
      h: 4.6,
      fill: { color: CARD_BG },
      line: { color: 'E2E8F0', width: 1 },
    });

    // Bullets
    const bulletItems = (slide.bullets || []).map((bullet: Claim | string) => {
      if (typeof bullet === 'string') {
        return {
          text: bullet,
          options: {
            bullet: true,
            fontSize: 15,
            color: TEXT_PRIMARY,
            paraSpaceAfter: 18,
            fontFace: 'Arial',
          },
        };
      }

      const provLabel = PROVENANCE_LABELS[bullet.provenance] || bullet.provenance;
      return {
        text: `${bullet.text}  [${provLabel}]`,
        options: {
          bullet: true,
          fontSize: 15,
          color: TEXT_PRIMARY,
          paraSpaceAfter: 18,
          fontFace: 'Arial',
        },
      };
    });

    if (bulletItems.length > 0) {
      s.addText(bulletItems, {
        x: 1.2,
        y: 2.2,
        w: 10.9,
        h: 3.8,
      });
    } else {
      s.addText('Not provided — requires validation', {
        x: 1.2,
        y: 2.5,
        w: 10.9,
        h: 1.0,
        fontSize: 16,
        italic: true,
        color: 'D97706',
      });
    }

    // Footer
    s.addText(`${startupName} | Confidential Investor Presentation`, {
      x: 0.8,
      y: 6.8,
      w: 6.0,
      h: 0.4,
      fontSize: 10,
      color: TEXT_SECONDARY,
    });
  });

  // Save file
  const fileName = `${startupName.replace(/\s+/g, '_')}_Pitch_Deck.pptx`;
  await pres.writeFile({ fileName });
}
