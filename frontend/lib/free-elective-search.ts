import { searchCatalogCourses } from "./api";
import type { CourseSearchResult } from "./types";

export const FREE_ELECTIVE_SEARCH_MIN_LENGTH = 2;
export const FREE_ELECTIVE_SEARCH_LIMIT = 50;
export const FREE_ELECTIVE_SEARCH_DEBOUNCE_MS = 180;

type CatalogSearch = (query: string, limit?: number, offset?: number) => Promise<CourseSearchResult[]>;

export function normalizeFreeElectiveSearchQuery(query: string): string {
  return query.trim();
}

export function shouldSearchFreeElectiveCatalog(query: string): boolean {
  return normalizeFreeElectiveSearchQuery(query).length >= FREE_ELECTIVE_SEARCH_MIN_LENGTH;
}

export async function searchFreeElectiveCatalog(
  query: string,
  search: CatalogSearch = searchCatalogCourses,
  offset = 0,
): Promise<CourseSearchResult[]> {
  const trimmed = normalizeFreeElectiveSearchQuery(query);
  if (trimmed && !shouldSearchFreeElectiveCatalog(trimmed)) return [];

  try {
    return await search(trimmed, FREE_ELECTIVE_SEARCH_LIMIT, offset);
  } catch {
    return [];
  }
}
