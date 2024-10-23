import unittest
from rufus.crawler import Crawler


class TestCrawler(unittest.TestCase):
    def test_bu_crawler(self):
        # Expected URLs
        expected_urls = {
            'https://www.bu.edu/cs/masters/program/', 
            'https://www.bu.edu/cs/research-groups/', 
            'https://www.bu.edu/cs/', 
            'https://www.bu.edu/cs/research-groups/networks/', 
            'https://www.bu.edu/cs/masters/program/#main', 
            'https://www.bu.edu/cs/research-groups/data-group/', 
            'https://www.bu.edu/cs/research-groups/ml/', 
            'https://www.bu.edu/cs/research-groups/vg/', 
            'https://www.bu.edu/cs/research-groups/theory/', 
            'https://www.bu.edu/cs/research-groups/popv/', 
            'https://www.bu.edu/cs/research-groups/systems/', 
            'https://www.bu.edu/cs/fsrp/', 
            'https://www.bu.edu/cs/research-groups/security/', 
            'https://www.bu.edu/cs/research-groups/grants-2/', 
            'https://www.bu.edu/cs/undergraduate/', 
            'https://www.bu.edu/cs/undergraduate/academic-programs/', 
            'https://www.bu.edu/cs/undergraduate/courses/', 
            'https://www.bu.edu/cs/undergraduate/undergraduate-life/', 
            'https://www.bu.edu/cs/masters/', 
            'https://www.bu.edu/cs/masters/admissions/', 
            'https://www.bu.edu/cs/faculty-awards/', 
            'https://www.bu.edu/cs/phd-program/', 
            'https://www.bu.edu/cs/phd-program/phd/', 
            'https://www.bu.edu/cs/phd-program/phd-program-milestones/', 
            'https://www.bu.edu/cs/phd-program/resources/', 
            'https://www.bu.edu/cs/people/', 
            'https://www.bu.edu/cs/people/faculty/', 
            'https://www.bu.edu/cs/people/faculty-leadership/', 
            'https://www.bu.edu/cs/people/department-staff/', 
            'https://www.bu.edu/cs/people/researchers/', 
            'https://www.bu.edu/cs/people/alumni/', 
            'https://www.bu.edu/cs/people/diversity/', 
            'https://www.bu.edu/cs/engage/', 
            'https://www.bu.edu/cs/engage/events-calendar/', 
            'https://www.bu.edu/cs/engage/careers/', 
            'https://www.bu.edu/cs/masters/resources/', 
            'https://www.bu.edu/cs/engage/news-tip/', 
            'https://www.bu.edu/cs/engage/newsletter/', 
            'https://www.bu.edu/cs/engage/ur2phd/', 
            'https://www.bu.edu/cs/engage/about/', 
            'https://www.bu.edu/cs/engage/give-back/', 
            'https://www.bu.edu/cs/masters/program/cs/data-centric/', 
            'https://www.bu.edu/cs/masters/program/ai/', 
            'https://www.bu.edu/cs/masters/program/cs/', 
            'https://www.bu.edu/cs/masters/program/cs/cyber-security/', 
            'https://www.bu.edu/cs/masters/program/faq/', 
            'https://www.bu.edu/cs/2024/09/30/grad-students-can-become-a-judge-for-upcoming-spark-hackathons/', 
            'https://www.bu.edu/cs/2024/10/15/bu-cs-opens-search-for-new-faculty-members/', 
            'https://www.bu.edu/cs/2024/03/15/grs-graduate-internship-funding-program-gif/', 
            'https://www.bu.edu/cs/2024/05/21/bucs-celebrated-the-class-of-2024-at-the-annual-computer-science-convocation/', 
            'https://www.bu.edu/cs/2024/02/20/boston-university-summer-term-high-school-programs-seek-applications-for-computer-science-summer-challenge-instructors/', 
            'https://www.bu.edu/cs/news/calendar/?eid=299101', 
            'https://www.bu.edu/cs/news/calendar/', 
            'https://www.bu.edu/cs/news/calendar/?eid=299108', 
            'https://www.bu.edu/cs/news/calendar/?eid=299109', 
            'https://www.bu.edu/cs/news/calendar/?eid=299102', 
            'https://www.bu.edu/cs/news/calendar/?eid=299110', 
            'https://www.bu.edu/cas/'
        }
        
        # Initialize the crawler
        crawler = Crawler()
        base_url = "https://www.bu.edu/cs/masters/program/"
        
        # Crawl the website
        results = crawler.crawl(base_url, max_depth=3)
        
        # Get the set of crawled URLs
        crawled_urls = set(results.keys())
        
        # Assert that the expected URLs match the crawled URLs
        self.assertEqual(expected_urls, crawled_urls)
        print(f"Crawled {len(crawled_urls)} pages.")

# Run the test
if __name__ == '__main__':
    unittest.main()