// Example: load passport-photo-specs in Rust.
//
// Fetches from the public API at idphotosnap.com/api/specs.
//
// Cargo.toml deps:
//   reqwest = { version = "0.12", features = ["json", "blocking"] }
//   serde = { version = "1", features = ["derive"] }
//   serde_json = "1"
//
// Run: cargo run

use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct Document {
    id: String,
    name: String,
    slug: String,
    #[serde(rename = "widthMm")]
    width_mm: u32,
    #[serde(rename = "heightMm")]
    height_mm: u32,
    #[serde(rename = "widthPx")]
    width_px: u32,
    #[serde(rename = "heightPx")]
    height_px: u32,
    dpi: u32,
    background: String,
    #[serde(rename = "bgColor")]
    bg_color: String,
    #[serde(rename = "bgColorLabel")]
    bg_color_label: String,
    requirements: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct Country {
    id: String,
    name: String,
    flag: String,
    documents: Vec<Document>,
}

#[derive(Debug, Deserialize)]
struct Response {
    countries: Vec<Country>,
}

fn fetch_specs(country: Option<&str>) -> Result<Response, Box<dyn std::error::Error>> {
    let mut url = String::from("https://idphotosnap.com/api/specs?format=raw");
    if let Some(c) = country {
        url.push_str("&country=");
        url.push_str(c);
    }
    let resp: Response = reqwest::blocking::get(&url)?.json()?;
    Ok(resp)
}

fn find_document<'a>(data: &'a Response, slug: &str) -> Option<(&'a Document, &'a Country)> {
    for country in &data.countries {
        for doc in &country.documents {
            if doc.slug == slug {
                return Some((doc, country));
            }
        }
    }
    None
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Example 1: filter to UK
    println!("=== UK document specs ===");
    let uk = fetch_specs(Some("uk"))?;
    for country in &uk.countries {
        for doc in &country.documents {
            println!(
                "  {:30} {}x{}mm  bg={}",
                doc.name, doc.width_mm, doc.height_mm, doc.bg_color_label
            );
        }
    }

    // Example 2: lookup Indian Sarathi driving license
    println!("\n=== India driving license lookup ===");
    let all = fetch_specs(None)?;
    if let Some((doc, country)) = find_document(&all, "india-driving-license-photo") {
        println!("  {} {}: {}x{}mm", country.name, doc.name, doc.width_mm, doc.height_mm);
        println!("  Pixel dims @ {} DPI: {}x{}", doc.dpi, doc.width_px, doc.height_px);
        println!("  Background: {}", doc.background);
        println!("  Top 3 requirements:");
        for req in doc.requirements.iter().take(3) {
            println!("    - {}", req);
        }
    }

    // Example 3: count all documents by background color
    println!("\n=== Document count by background color ===");
    let mut counts = std::collections::HashMap::new();
    for country in &all.countries {
        for doc in &country.documents {
            *counts.entry(doc.bg_color_label.clone()).or_insert(0u32) += 1;
        }
    }
    let mut sorted: Vec<_> = counts.iter().collect();
    sorted.sort_by(|a, b| b.1.cmp(a.1));
    for (color, count) in sorted {
        println!("  {:20} {}", color, count);
    }

    Ok(())
}
