from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'royal-quiz-platform-2024'

def init_db():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('DROP TABLE IF EXISTS questions')
    c.execute('DROP TABLE IF EXISTS results')
    
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT, created_at TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS questions 
                 (id INTEGER PRIMARY KEY, question TEXT, option_a TEXT, option_b TEXT, 
                  option_c TEXT, option_d TEXT, correct_answer TEXT, category TEXT, difficulty TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS results 
                 (id INTEGER PRIMARY KEY, user_id INTEGER, score INTEGER, total INTEGER, 
                  category TEXT, difficulty TEXT, percentage REAL, date TEXT, time_taken TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # ============ MASSIVE QUESTION BANK (40+ per category, 4 difficulties) ============
    questions = [
        # PYTHON (44 Questions)
        ('What is Python?', 'A snake', 'Programming language', 'A fruit', 'A city', 'B', 'Python', 'Very Easy'),
        ('Which keyword defines a function?', 'def', 'function', 'func', 'define', 'A', 'Python', 'Very Easy'),
        ('How to print text?', 'print()', 'echo()', 'write()', 'show()', 'A', 'Python', 'Very Easy'),
        ('What symbol starts a comment?', '#', '//', '/*', '--', 'A', 'Python', 'Very Easy'),
        ('Which is a variable name?', 'my_var', '2var', 'var-name', 'var name', 'A', 'Python', 'Very Easy'),
        ('Python is:', 'Compiled', 'Interpreted', 'Both', 'None', 'B', 'Python', 'Easy'),
        ('What does OOP stand for?', 'Object Oriented Programming', 'Oriented Object Programming', 'Object Operational Programming', 'Operational Oriented Programming', 'A', 'Python', 'Easy'),
        ('Output of print(2**3)?', '6', '8', '9', '5', 'B', 'Python', 'Easy'),
        ('Which is immutable?', 'List', 'Dictionary', 'Tuple', 'Set', 'C', 'Python', 'Easy'),
        ('How to get length of list?', 'len()', 'size()', 'count()', 'length()', 'A', 'Python', 'Easy'),
        ('What does break do?', 'Exit loop', 'Continue loop', 'Define function', 'Import module', 'A', 'Python', 'Easy'),
        ('Which library for data science?', 'Pandas', 'Flask', 'Django', 'Requests', 'A', 'Python', 'Easy'),
        ('What is pip?', 'Package installer', 'Code editor', 'Database', 'Compiler', 'A', 'Python', 'Easy'),
        ('What is __init__?', 'Constructor', 'Destructor', 'Module', 'Package', 'A', 'Python', 'Medium'),
        ('Which module handles JSON?', 'json', 'xml', 'csv', 'pickle', 'A', 'Python', 'Medium'),
        ('What does PEP 8 define?', 'Coding style', 'Error handling', 'Database', 'Networking', 'A', 'Python', 'Medium'),
        ('List comprehension syntax?', '[x for x in list]', '{x for x}', '(x for x)', '<x for x>', 'A', 'Python', 'Medium'),
        ('What is GIL?', 'Global Interpreter Lock', 'General Input Loop', 'Graph Integration Layer', 'None', 'A', 'Python', 'Medium'),
        ('Which is NOT a core data type?', 'List', 'Dictionary', 'Array', 'Tuple', 'C', 'Python', 'Medium'),
        ('How to handle exceptions?', 'try-except', 'if-else', 'for-while', 'switch-case', 'A', 'Python', 'Medium'),
        ('What does *args do?', 'Variable positional args', 'Keyword args', 'File args', 'None', 'A', 'Python', 'Medium'),
        ('Which decorator caches results?', '@cache', '@memoize', '@store', '@save', 'A', 'Python', 'Medium'),
        ('What is a generator?', 'Function yielding values', 'Class instance', 'Module', 'Package', 'A', 'Python', 'Medium'),
        ('What does super() do?', 'Call parent class', 'Call child class', 'Define variable', 'Import module', 'A', 'Python', 'Medium'),
        ('Which method is called on object creation?', '__init__', '__new__', '__call__', '__str__', 'A', 'Python', 'Hard'),
        ('What is metaclass?', 'Class of a class', 'Data type', 'Function', 'Module', 'A', 'Python', 'Hard'),
        ('How does garbage collection work?', 'Reference counting + GC', 'Manual only', 'No GC', 'Stack only', 'A', 'Python', 'Hard'),
        ('What is __slots__?', 'Memory optimization', 'Thread lock', 'File handler', 'Network port', 'A', 'Python', 'Hard'),
        ('Which is faster: list or tuple?', 'Tuple', 'List', 'Same', 'Depends', 'A', 'Python', 'Hard'),
        ('What does @staticmethod do?', 'No self/cls needed', 'Requires self', 'Private method', 'Abstract method', 'A', 'Python', 'Hard'),
        ('What is monkey patching?', 'Runtime modification', 'Class inheritance', 'File I/O', 'Network call', 'A', 'Python', 'Hard'),
        ('How to create virtual env?', 'python -m venv', 'pip venv', 'conda env', 'venv create', 'A', 'Python', 'Hard'),
        ('What is PEP 517?', 'Build system standard', 'Coding style', 'Error format', 'Import rule', 'A', 'Python', 'Hard'),
        ('Which library for async?', 'asyncio', 'threading', 'multiprocessing', 'concurrent', 'A', 'Python', 'Hard'),
        ('What is descriptor protocol?', '__get__/__set__', '__init__/__del__', '__str__/__repr__', '__enter__/__exit__', 'A', 'Python', 'Hard'),
        ('How to profile code?', 'cProfile', 'timeit', 'profile', 'measure', 'A', 'Python', 'Hard'),
        ('What is __all__?', 'Public API list', 'All variables', 'Import all', 'Export all', 'A', 'Python', 'Hard'),
        ('Which is thread-safe?', 'queue.Queue', 'list', 'dict', 'set', 'A', 'Python', 'Hard'),
        ('What does __name__ == "__main__" check?', 'Entry point', 'Module name', 'File path', 'Import status', 'A', 'Python', 'Hard'),
        ('How to freeze dependencies?', 'pip freeze > req.txt', 'pip list', 'pip show', 'pip export', 'A', 'Python', 'Hard'),
        ('What is MRO?', 'Method Resolution Order', 'Memory Run Option', 'Module Run Order', 'Method Run Output', 'A', 'Python', 'Hard'),
        ('Which hook runs before import?', '__import__', '__load__', '__fetch__', '__get__', 'A', 'Python', 'Hard'),
        ('What is __pycache__?', 'Compiled bytecode', 'Source code', 'Config file', 'Log file', 'A', 'Python', 'Hard'),
        ('How to handle large files?', 'Iterate line by line', 'Read all at once', 'Split manually', 'Compress first', 'A', 'Python', 'Hard'),
        
        # WEB DEV (42 Questions)
        ('HTML stands for?', 'Hyper Text Markup Language', 'High Text Machine', 'Hyperlink Transfer', 'Home Tool Markup', 'A', 'Web Dev', 'Very Easy'),
        ('Which tag creates paragraph?', '<p>', '<div>', '<span>', '<para>', 'A', 'Web Dev', 'Very Easy'),
        ('How to create link?', '<a href>', '<link>', '<href>', '<url>', 'A', 'Web Dev', 'Very Easy'),
        ('Which tag for image?', '<img>', '<pic>', '<photo>', '<image>', 'A', 'Web Dev', 'Very Easy'),
        ('What is DOCTYPE?', 'Document type declaration', 'Data type', 'File format', 'Browser tag', 'A', 'Web Dev', 'Very Easy'),
        ('CSS property for text color?', 'color', 'text-color', 'font-color', 'style', 'A', 'Web Dev', 'Easy'),
        ('What does JS stand for?', 'JavaScript', 'JavaSource', 'JustScript', 'JavaSystem', 'A', 'Web Dev', 'Easy'),
        ('Which CSS layout is flexible?', 'Flexbox', 'Table', 'Div', 'Span', 'A', 'Web Dev', 'Easy'),
        ('How to link CSS file?', '<link>', '<style>', '<css>', '<import>', 'A', 'Web Dev', 'Easy'),
        ('Which event fires on click?', 'onclick', 'onhover', 'onload', 'onsubmit', 'A', 'Web Dev', 'Easy'),
        ('What is DOM?', 'Document Object Model', 'Data Object Mode', 'Digital Output Module', 'None', 'A', 'Web Dev', 'Easy'),
        ('Which selector targets ID?', '#', '.', '*', '>', 'A', 'Web Dev', 'Easy'),
        ('What does API stand for?', 'Application Programming Interface', 'Advanced Program Input', 'App Process Integration', 'None', 'A', 'Web Dev', 'Easy'),
        ('Which HTTP method sends data?', 'POST', 'GET', 'PUT', 'DELETE', 'A', 'Web Dev', 'Easy'),
        ('What is responsive design?', 'Adapts to screen size', 'Fast loading', 'Secure', 'Animated', 'A', 'Web Dev', 'Easy'),
        ('What is semantic HTML?', 'Meaningful tags', 'Faster loading', 'SEO only', 'JS enabled', 'A', 'Web Dev', 'Medium'),
        ('Which framework is JS-based?', 'React', 'Flask', 'Django', 'Spring', 'A', 'Web Dev', 'Medium'),
        ('What does CDN stand for?', 'Content Delivery Network', 'Code Development Node', 'Cloud Data Network', 'None', 'A', 'Web Dev', 'Medium'),
        ('Which tag embeds video?', '<video>', '<media>', '<play>', '<movie>', 'A', 'Web Dev', 'Medium'),
        ('What is localhost?', 'Your own machine', 'Remote server', 'Cloud', 'DNS', 'A', 'Web Dev', 'Medium'),
        ('What is CORS?', 'Cross-Origin Resource Sharing', 'Code Origin Rule System', 'Client Object Request Security', 'None', 'A', 'Web Dev', 'Medium'),
        ('Which storage is persistent?', 'localStorage', 'sessionStorage', 'cookie', 'cache', 'A', 'Web Dev', 'Medium'),
        ('What is SSR?', 'Server-Side Rendering', 'Secure Socket Response', 'Static Site Router', 'System Service Run', 'A', 'Web Dev', 'Medium'),
        ('Which tool bundles JS?', 'Webpack', 'NPM', 'Git', 'Docker', 'A', 'Web Dev', 'Medium'),
        ('What is progressive enhancement?', 'Base HTML + JS/CSS layers', 'Mobile first', 'Dark mode', 'SEO optimization', 'A', 'Web Dev', 'Medium'),
        ('How to prevent XSS?', 'Escape output', 'Use HTTPS', 'Minify JS', 'Compress CSS', 'A', 'Web Dev', 'Medium'),
        ('What is shadow DOM?', 'Encapsulated DOM tree', 'Hidden CSS', 'Private JS', 'Secure API', 'A', 'Web Dev', 'Medium'),
        ('Which protocol is secure?', 'HTTPS', 'HTTP', 'FTP', 'SMTP', 'A', 'Web Dev', 'Hard'),
        ('What is HTTP/2 feature?', 'Multiplexing', 'Plain text', 'No compression', 'Stateless only', 'A', 'Web Dev', 'Hard'),
        ('What is service worker?', 'Background script', 'Database', 'Server', 'Framework', 'A', 'Web Dev', 'Hard'),
        ('What is virtual DOM?', 'JS representation of DOM', 'Real DOM', 'CSS engine', 'Server cache', 'A', 'Web Dev', 'Hard'),
        ('How to optimize images?', 'WebP format + lazy load', 'PNG always', 'No compression', 'Base64 only', 'A', 'Web Dev', 'Hard'),
        ('What is CSP?', 'Content Security Policy', 'Client Side Protocol', 'Cache Storage Path', 'Cross Site Plugin', 'A', 'Web Dev', 'Hard'),
        ('What is hydration?', 'Attach event listeners to SSR HTML', 'Download JS', 'Clear cache', 'Reload page', 'A', 'Web Dev', 'Hard'),
        ('Which header prevents clickjacking?', 'X-Frame-Options', 'Content-Type', 'Accept', 'User-Agent', 'A', 'Web Dev', 'Hard'),
        ('What is tree shaking?', 'Remove unused code', 'Sort DOM', 'Compress CSS', 'Cache images', 'A', 'Web Dev', 'Hard'),
        ('What is micro-frontend?', 'Independent frontend modules', 'Single page app', 'Backend API', 'Database shard', 'A', 'Web Dev', 'Hard'),
        ('How to handle state in React?', 'useState/useReducer', 'localStorage only', 'Global variables', 'Cookie', 'A', 'Web Dev', 'Hard'),
        ('What is critical CSS?', 'Above-fold styles', 'All CSS', 'JS styles', 'Print styles', 'A', 'Web Dev', 'Hard'),
        ('What is prefetching?', 'Load resources before needed', 'Compress files', 'Cache headers', 'Minify code', 'A', 'Web Dev', 'Hard'),
        ('What is layout shift?', 'Unexpected visual change', 'Smooth animation', 'Responsive grid', 'Flexbox wrap', 'A', 'Web Dev', 'Hard'),
        ('How to improve CLS?', 'Set width/height on media', 'Remove CSS', 'Use JS only', 'Disable fonts', 'A', 'Web Dev', 'Hard'),
        
        # DBMS (40 Questions)
        ('SQL stands for?', 'Structured Query Language', 'Strong Question Lang', 'Simple Query Lang', 'None', 'A', 'DBMS', 'Very Easy'),
        ('Which command retrieves data?', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'A', 'DBMS', 'Very Easy'),
        ('How to create table?', 'CREATE TABLE', 'NEW TABLE', 'MAKE TABLE', 'ADD TABLE', 'A', 'DBMS', 'Very Easy'),
        ('Which clause filters rows?', 'WHERE', 'GROUP BY', 'ORDER BY', 'HAVING', 'A', 'DBMS', 'Very Easy'),
        ('What is primary key?', 'Unique identifier', 'Foreign reference', 'Table name', 'Index', 'A', 'DBMS', 'Very Easy'),
        ('Which normal form removes partial dependency?', '2NF', '1NF', '3NF', 'BCNF', 'A', 'DBMS', 'Easy'),
        ('What does ACID stand for?', 'Atomicity Consistency Isolation Durability', 'Accuracy Consistency Integration Durability', 'Atomicity Concurrency Isolation Durability', 'None', 'A', 'DBMS', 'Easy'),
        ('Which clause filters groups?', 'HAVING', 'WHERE', 'GROUP', 'ORDER', 'A', 'DBMS', 'Easy'),
        ('What is a View?', 'Virtual table', 'Physical table', 'Index', 'Procedure', 'A', 'DBMS', 'Easy'),
        ('Which join returns all from left?', 'LEFT JOIN', 'INNER JOIN', 'RIGHT JOIN', 'FULL JOIN', 'A', 'DBMS', 'Easy'),
        ('What is indexing used for?', 'Faster search', 'Data encryption', 'Backup', 'Compression', 'A', 'DBMS', 'Easy'),
        ('Which language defines schema?', 'DDL', 'DML', 'DCL', 'TCL', 'A', 'DBMS', 'Easy'),
        ('What is a transaction?', 'Logical unit of work', 'Table structure', 'User login', 'Backup', 'A', 'DBMS', 'Easy'),
        ('Which constraint ensures uniqueness?', 'UNIQUE', 'PRIMARY', 'NOT NULL', 'CHECK', 'A', 'DBMS', 'Easy'),
        ('What is normalization?', 'Reduce redundancy', 'Increase speed', 'Encrypt data', 'Backup', 'A', 'DBMS', 'Easy'),
        ('What is denormalization?', 'Add redundancy for speed', 'Remove tables', 'Encrypt data', 'Compress rows', 'A', 'DBMS', 'Medium'),
        ('Which isolation level prevents dirty reads?', 'Read Committed', 'Read Uncommitted', 'Repeatable Read', 'Serializable', 'A', 'DBMS', 'Medium'),
        ('What is a trigger?', 'Auto-executed procedure', 'Table', 'Index', 'View', 'A', 'DBMS', 'Medium'),
        ('Which index type is default?', 'B-Tree', 'Hash', 'Bitmap', 'Full-text', 'A', 'DBMS', 'Medium'),
        ('What is sharding?', 'Horizontal partitioning', 'Vertical scaling', 'Encryption', 'Backup', 'A', 'DBMS', 'Medium'),
        ('What is replication?', 'Copy data to multiple nodes', 'Delete data', 'Compress data', 'Sort data', 'A', 'DBMS', 'Medium'),
        ('Which query returns duplicates?', 'SELECT without DISTINCT', 'SELECT DISTINCT', 'JOIN', 'UNION', 'A', 'DBMS', 'Medium'),
        ('What is a cursor?', 'Database pointer', 'Table', 'Index', 'View', 'A', 'DBMS', 'Medium'),
        ('Which command modifies structure?', 'ALTER', 'UPDATE', 'MODIFY', 'CHANGE', 'A', 'DBMS', 'Medium'),
        ('What is deadlock?', 'Two transactions wait for each other', 'Fast query', 'Index corruption', 'Backup failure', 'A', 'DBMS', 'Medium'),
        ('How to resolve deadlock?', 'Rollback one transaction', 'Restart DB', 'Delete table', 'Compress data', 'A', 'DBMS', 'Medium'),
        ('What is materialized view?', 'Pre-computed query result', 'Temporary table', 'Index', 'Trigger', 'A', 'DBMS', 'Hard'),
        ('Which algorithm handles joins efficiently?', 'Hash Join', 'Nested Loop', 'Sort Merge', 'Index Scan', 'A', 'DBMS', 'Hard'),
        ('What is WAL?', 'Write-Ahead Logging', 'Write After Lock', 'Web Access Layer', 'Wide Area Link', 'A', 'DBMS', 'Hard'),
        ('What is MVCC?', 'Multi-Version Concurrency Control', 'Multi-View Cache Control', 'Memory Version Check', 'Module Version Config', 'A', 'DBMS', 'Hard'),
        ('Which isolation prevents phantom reads?', 'Serializable', 'Read Committed', 'Repeatable Read', 'Read Uncommitted', 'A', 'DBMS', 'Hard'),
        ('What is covering index?', 'Contains all queried columns', 'Primary key only', 'Foreign key', 'Full table', 'A', 'DBMS', 'Hard'),
        ('How to optimize slow query?', 'EXPLAIN + index', 'Delete data', 'Increase RAM', 'Restart server', 'A', 'DBMS', 'Hard'),
        ('What is partition pruning?', 'Skip irrelevant partitions', 'Delete old data', 'Compress rows', 'Sort columns', 'A', 'DBMS', 'Hard'),
        ('What is optimistic locking?', 'Check version before update', 'Lock table', 'Block writes', 'Queue requests', 'A', 'DBMS', 'Hard'),
        ('Which cache stores query results?', 'Query Cache', 'Buffer Pool', 'Log Cache', 'Index Cache', 'A', 'DBMS', 'Hard'),
        ('What is tuple movement?', 'Row relocation during update', 'Index rebuild', 'Backup copy', 'Log write', 'A', 'DBMS', 'Hard'),
        ('How to handle concurrent inserts?', 'Auto-increment + lock', 'Manual ID', 'Random ID', 'Skip ID', 'A', 'DBMS', 'Hard'),
        ('What is buffer pool?', 'In-memory data cache', 'Disk storage', 'Network buffer', 'Log file', 'A', 'DBMS', 'Hard'),
        ('Which checkpoint ensures durability?', 'Full checkpoint', 'Partial', 'Async', 'Lazy', 'A', 'DBMS', 'Hard'),
        
        # JAVA (42 Questions)
        ('Java is:', 'Platform Independent', 'Platform Dependent', 'Both', 'None', 'A', 'Java', 'Very Easy'),
        ('Who developed Java?', 'Sun Microsystems', 'Microsoft', 'IBM', 'Apple', 'A', 'Java', 'Very Easy'),
        ('Which keyword inherits class?', 'extends', 'inherits', 'implements', 'uses', 'A', 'Java', 'Very Easy'),
        ('What is JVM?', 'Java Virtual Machine', 'Java Visual Mode', 'Java Version Manager', 'None', 'A', 'Java', 'Very Easy'),
        ('How to print output?', 'System.out.println()', 'print()', 'echo()', 'write()', 'A', 'Java', 'Very Easy'),
        ('Which is not a primitive type?', 'String', 'int', 'float', 'boolean', 'A', 'Java', 'Easy'),
        ('What does main method return?', 'void', 'int', 'String', 'null', 'A', 'Java', 'Easy'),
        ('Which block handles errors?', 'try-catch', 'if-else', 'for-while', 'switch', 'A', 'Java', 'Easy'),
        ('What is interface?', 'Abstract type', 'Concrete class', 'Package', 'Module', 'A', 'Java', 'Easy'),
        ('Which keyword prevents inheritance?', 'final', 'static', 'private', 'protected', 'A', 'Java', 'Easy'),
        ('What is garbage collection?', 'Memory management', 'File deletion', 'Cache clear', 'None', 'A', 'Java', 'Easy'),
        ('Which collection allows duplicates?', 'List', 'Set', 'Map', 'Queue', 'A', 'Java', 'Easy'),
        ('What does super do?', 'Call parent constructor', 'Call child', 'Define variable', 'Import class', 'A', 'Java', 'Easy'),
        ('What is package?', 'Namespace organizer', 'Method', 'Variable', 'Class', 'A', 'Java', 'Easy'),
        ('Which access modifier is most restrictive?', 'private', 'public', 'protected', 'default', 'A', 'Java', 'Easy'),
        ('What is polymorphism?', 'One interface, multiple forms', 'Single form', 'No inheritance', 'Static binding', 'A', 'Java', 'Medium'),
        ('Which thread method starts execution?', 'start()', 'run()', 'execute()', 'begin()', 'A', 'Java', 'Medium'),
        ('What is synchronized?', 'Thread-safe block', 'Fast execution', 'Memory leak', 'Compile error', 'A', 'Java', 'Medium'),
        ('Which collection is thread-safe?', 'Vector', 'ArrayList', 'LinkedList', 'HashSet', 'A', 'Java', 'Medium'),
        ('What is lambda expression?', 'Anonymous function', 'Class instance', 'Package', 'Module', 'A', 'Java', 'Medium'),
        ('Which stream operation is terminal?', 'collect()', 'filter()', 'map()', 'sorted()', 'A', 'Java', 'Medium'),
        ('What is Optional?', 'Null-safe container', 'Thread pool', 'File handler', 'Network socket', 'A', 'Java', 'Medium'),
        ('How to create immutable class?', 'final fields + no setters', 'public fields', 'static methods', 'volatile vars', 'A', 'Java', 'Medium'),
        ('What is reflection?', 'Inspect/modify at runtime', 'Compile time check', 'Memory allocation', 'Thread sync', 'A', 'Java', 'Medium'),
        ('Which GC algorithm is default?', 'G1GC', 'Serial', 'Parallel', 'CMS', 'A', 'Java', 'Medium'),
        ('What is classloader?', 'Loads classes into JVM', 'Compiles code', 'Runs threads', 'Manages memory', 'A', 'Java', 'Medium'),
        ('What is JIT compiler?', 'Just-In-Time compilation', 'Java Input Tool', 'Joint Integration Test', 'Java Interface Template', 'A', 'Java', 'Medium'),
        ('What is method overloading?', 'Same name, different params', 'Same name, same params', 'Different name', 'No params', 'A', 'Java', 'Hard'),
        ('What is diamond problem?', 'Multiple inheritance ambiguity', 'Memory leak', 'Thread deadlock', 'Compile error', 'A', 'Java', 'Hard'),
        ('How does HashMap handle collisions?', 'Chaining/Treeify', 'Delete key', 'Stop insert', 'Resize only', 'A', 'Java', 'Hard'),
        ('What is volatile keyword?', 'Visibility guarantee', 'Thread lock', 'Memory allocation', 'Compile flag', 'A', 'Java', 'Hard'),
        ('What is CompletableFuture?', 'Async programming API', 'Sync call', 'Database query', 'File I/O', 'A', 'Java', 'Hard'),
        ('What is module system?', 'Java 9+ JPMS', 'Package manager', 'Thread pool', 'Memory heap', 'A', 'Java', 'Hard'),
        ('How to avoid memory leak?', 'Null references + close resources', 'Increase heap', 'Use static', 'Skip GC', 'A', 'Java', 'Hard'),
        ('What is record class?', 'Immutable data carrier', 'Mutable class', 'Abstract type', 'Interface', 'A', 'Java', 'Hard'),
        ('What is sealed class?', 'Restricted inheritance', 'Public class', 'Final class', 'Static class', 'A', 'Java', 'Hard'),
        ('What is pattern matching?', 'Type check + cast', 'Loop control', 'Exception handling', 'Thread sync', 'A', 'Java', 'Hard'),
        ('What is virtual thread?', 'Lightweight thread', 'Heavy thread', 'Daemon thread', 'System thread', 'A', 'Java', 'Hard'),
        ('How to tune JVM?', '-Xmx/-Xms flags', 'Delete classes', 'Skip GC', 'Use int only', 'A', 'Java', 'Hard'),
        ('What is GraalVM?', 'Polyglot runtime + AOT', 'Java compiler', 'DB driver', 'Web server', 'A', 'Java', 'Hard'),
        ('What is ZGC?', 'Low-latency GC', 'High-throughput GC', 'Serial GC', 'Parallel GC', 'A', 'Java', 'Hard'),
        ('How to handle backpressure?', 'Flow control + buffers', 'Drop data', 'Block thread', 'Restart JVM', 'A', 'Java', 'Hard'),
        
        # DATA SCIENCE (40 Questions)
        ('What is Data Science?', 'Extract knowledge from data', 'Only statistics', 'Database management', 'Web dev', 'A', 'Data Science', 'Very Easy'),
        ('Which library for data manipulation?', 'Pandas', 'TensorFlow', 'Keras', 'PyTorch', 'A', 'Data Science', 'Very Easy'),
        ('What is Machine Learning?', 'Learn from data without explicit programming', 'Hardware learning', 'Manual coding', 'None', 'A', 'Data Science', 'Very Easy'),
        ('Which plot shows distribution?', 'Histogram', 'Pie chart', 'Line graph', 'Scatter', 'A', 'Data Science', 'Very Easy'),
        ('What is a dataset?', 'Collection of data', 'Single value', 'Algorithm', 'Model', 'A', 'Data Science', 'Very Easy'),
        ('What is EDA?', 'Exploratory Data Analysis', 'Extra Data Access', 'Engine Data Audit', 'None', 'A', 'Data Science', 'Easy'),
        ('Which library for visualization?', 'Matplotlib', 'NumPy', 'SciPy', 'Requests', 'A', 'Data Science', 'Easy'),
        ('What is feature engineering?', 'Creating useful features', 'Buying features', 'Deleting data', 'None', 'A', 'Data Science', 'Easy'),
        ('Which is dimensionality reduction?', 'PCA', 'SVM', 'KNN', 'RF', 'A', 'Data Science', 'Easy'),
        ('What is a model?', 'Mathematical representation', 'Database', 'UI', 'None', 'A', 'Data Science', 'Easy'),
        ('Which metric for classification?', 'Accuracy', 'MSE', 'R-squared', 'MAE', 'A', 'Data Science', 'Easy'),
        ('What is cross-validation?', 'Model evaluation technique', 'Data backup', 'Security check', 'None', 'A', 'Data Science', 'Easy'),
        ('What is unsupervised learning?', 'No labeled data', 'Labeled data', 'Reinforcement', 'Supervised', 'A', 'Data Science', 'Easy'),
        ('What is regression?', 'Predict continuous values', 'Classify categories', 'Cluster data', 'Reduce dimensions', 'A', 'Data Science', 'Easy'),
        ('What is classification?', 'Predict categories', 'Predict numbers', 'Group data', 'Sort data', 'A', 'Data Science', 'Easy'),
        ('What is overfitting?', 'Good on train, poor on test', 'Good on both', 'Poor on both', 'Perfect model', 'A', 'Data Science', 'Medium'),
        ('Which algorithm is for classification?', 'Decision Tree', 'K-Means', 'PCA', 'Linear Regression', 'A', 'Data Science', 'Medium'),
        ('What is gradient descent?', 'Optimization algorithm', 'Data collection', 'Visualization', 'Deployment', 'A', 'Data Science', 'Medium'),
        ('What is regularization?', 'Prevent overfitting', 'Speed up training', 'Increase accuracy', 'Reduce data', 'A', 'Data Science', 'Medium'),
        ('What is ensemble learning?', 'Combine multiple models', 'Single model', 'No model', 'Manual coding', 'A', 'Data Science', 'Medium'),
        ('What is hyperparameter tuning?', 'Optimize model settings', 'Clean data', 'Train model', 'Deploy model', 'A', 'Data Science', 'Medium'),
        ('What is bias-variance tradeoff?', 'Model complexity balance', 'Data size', 'Learning rate', 'Epoch count', 'A', 'Data Science', 'Medium'),
        ('What is confusion matrix?', 'Classification performance table', 'Data table', 'Feature list', 'Model code', 'A', 'Data Science', 'Medium'),
        ('What is ROC curve?', 'True/False positive rate plot', 'Loss curve', 'Accuracy plot', 'Data distribution', 'A', 'Data Science', 'Medium'),
        ('What is feature scaling?', 'Normalize/standardize features', 'Delete features', 'Add features', 'Sort features', 'A', 'Data Science', 'Medium'),
        ('What is bagging?', 'Bootstrap aggregating', 'Gradient boosting', 'Random sampling', 'Feature selection', 'A', 'Data Science', 'Hard'),
        ('What is XGBoost?', 'Optimized gradient boosting', 'Neural network', 'Clustering', 'Dimensionality reduction', 'A', 'Data Science', 'Hard'),
        ('What is transfer learning?', 'Reuse pre-trained model', 'Train from scratch', 'Delete model', 'Compress data', 'A', 'Data Science', 'Hard'),
        ('What is GAN?', 'Generative Adversarial Network', 'Graph Analysis Node', 'General Algorithm Network', 'Global Array Name', 'A', 'Data Science', 'Hard'),
        ('What is attention mechanism?', 'Focus on relevant parts', 'Ignore data', 'Random sampling', 'Full computation', 'A', 'Data Science', 'Hard'),
        ('What is backpropagation?', 'Gradient computation for weights', 'Data loading', 'Model saving', 'Feature extraction', 'A', 'Data Science', 'Hard'),
        ('What is vanishing gradient?', 'Small gradients stop learning', 'Fast learning', 'High accuracy', 'Low memory', 'A', 'Data Science', 'Hard'),
        ('What is batch normalization?', 'Stabilize training', 'Increase data', 'Reduce features', 'Compress model', 'A', 'Data Science', 'Hard'),
        ('What is dropout?', 'Randomly disable neurons', 'Add neurons', 'Sort data', 'Compress weights', 'A', 'Data Science', 'Hard'),
        ('What is Adam optimizer?', 'Adaptive learning rate', 'Fixed learning rate', 'No learning rate', 'Manual tuning', 'A', 'Data Science', 'Hard'),
        ('What is early stopping?', 'Stop when val loss increases', 'Train forever', 'Delete model', 'Increase epochs', 'A', 'Data Science', 'Hard'),
        ('What is data leakage?', 'Train info in test set', 'Secure data', 'Fast training', 'High accuracy', 'A', 'Data Science', 'Hard'),
        ('What is SHAP?', 'Model explanation framework', 'Data collection', 'Feature engineering', 'Deployment tool', 'A', 'Data Science', 'Hard'),
        ('What is MLOps?', 'ML lifecycle management', 'Data storage', 'UI design', 'Hardware setup', 'A', 'Data Science', 'Hard'),
        ('What is feature store?', 'Centralized feature repository', 'Model code', 'Training script', 'UI component', 'A', 'Data Science', 'Hard'),
        
        # NETWORKING (40 Questions)
        ('HTTP stands for?', 'HyperText Transfer Protocol', 'HighText Transfer', 'HyperText Transmission', 'None', 'A', 'Networking', 'Very Easy'),
        ('Default port for HTTPS?', '443', '80', '8080', '21', 'A', 'Networking', 'Very Easy'),
        ('What is IP address?', 'Device identifier on network', 'Password', 'Username', 'MAC address', 'A', 'Networking', 'Very Easy'),
        ('What does DNS do?', 'Domain to IP mapping', 'Email routing', 'File transfer', 'Encryption', 'A', 'Networking', 'Very Easy'),
        ('What is ping used for?', 'Test connectivity', 'Download file', 'Send email', 'Browse web', 'A', 'Networking', 'Very Easy'),
        ('Which layer handles routing?', 'Network', 'Transport', 'Data Link', 'Application', 'A', 'Networking', 'Easy'),
        ('Which protocol is connectionless?', 'UDP', 'TCP', 'HTTP', 'FTP', 'A', 'Networking', 'Easy'),
        ('Which device connects networks?', 'Router', 'Hub', 'Switch', 'Bridge', 'A', 'Networking', 'Easy'),
        ('What is subnet mask?', 'Divides IP into network/host', 'Encryption key', 'Password', 'MAC', 'A', 'Networking', 'Easy'),
        ('Which OSI layer is physical?', 'Layer 1', 'Layer 2', 'Layer 3', 'Layer 4', 'A', 'Networking', 'Easy'),
        ('What is firewall?', 'Network security system', 'Web browser', 'Database', 'Compiler', 'A', 'Networking', 'Easy'),
        ('Which protocol secures web?', 'TLS/SSL', 'FTP', 'SMTP', 'POP3', 'A', 'Networking', 'Easy'),
        ('What is bandwidth?', 'Data transfer capacity', 'Security level', 'Latency', 'Protocol', 'A', 'Networking', 'Easy'),
        ('Which IP version is 128-bit?', 'IPv6', 'IPv4', 'IPv5', 'IPv3', 'A', 'Networking', 'Easy'),
        ('What is DHCP?', 'Dynamic IP assignment', 'Static IP', 'DNS lookup', 'Firewall rule', 'A', 'Networking', 'Easy'),
        ('What is NAT?', 'Private to public IP translation', 'Data encryption', 'Packet filtering', 'Load balancing', 'A', 'Networking', 'Medium'),
        ('What is ARP?', 'IP to MAC resolution', 'DNS lookup', 'Route calculation', 'Packet encryption', 'A', 'Networking', 'Medium'),
        ('What is BGP?', 'Inter-domain routing protocol', 'Email protocol', 'File transfer', 'Web standard', 'A', 'Networking', 'Medium'),
        ('What is VLAN?', 'Logical network segmentation', 'Physical cable', 'Firewall rule', 'DNS record', 'A', 'Networking', 'Medium'),
        ('What is QoS?', 'Traffic prioritization', 'Data compression', 'Encryption standard', 'Routing algorithm', 'A', 'Networking', 'Medium'),
        ('What is MTU?', 'Max packet size', 'Min packet size', 'Bandwidth limit', 'Latency threshold', 'A', 'Networking', 'Medium'),
        ('What is TTL?', 'Packet hop limit', 'Time to live server', 'Transfer type log', 'Traffic tracking level', 'A', 'Networking', 'Medium'),
        ('What is ICMP?', 'Error/diagnostic messages', 'File transfer', 'Email routing', 'Web browsing', 'A', 'Networking', 'Medium'),
        ('What is traceroute?', 'Path discovery tool', 'Speed test', 'DNS lookup', 'Firewall config', 'A', 'Networking', 'Medium'),
        ('What is load balancer?', 'Distribute traffic', 'Block traffic', 'Encrypt traffic', 'Cache traffic', 'A', 'Networking', 'Medium'),
        ('What is SDN?', 'Software-defined networking', 'Secure data network', 'System domain name', 'Standard data node', 'A', 'Networking', 'Hard'),
        ('What is VXLAN?', 'Network virtualization overlay', 'Physical cable', 'Firewall type', 'DNS protocol', 'A', 'Networking', 'Hard'),
        ('What is BGP hijacking?', 'Route manipulation attack', 'DNS spoofing', 'Packet loss', 'Bandwidth theft', 'A', 'Networking', 'Hard'),
        ('What is anycast?', 'Multiple servers, one IP', 'Single server', 'P2P network', 'Broadcast only', 'A', 'Networking', 'Hard'),
        ('What is ECMP?', 'Equal-cost multi-path routing', 'Single path routing', 'Load balancing only', 'Firewall rule', 'A', 'Networking', 'Hard'),
        ('What is TCP window scaling?', 'Increase throughput', 'Reduce latency', 'Encrypt data', 'Compress packets', 'A', 'Networking', 'Hard'),
        ('What is SYN flood?', 'DoS attack using half-open connections', 'Normal traffic', 'DNS query', 'Email spam', 'A', 'Networking', 'Hard'),
        ('What is BBR congestion control?', "Google's TCP algorithm", 'Cisco protocol', 'Linux firewall', 'DNS standard', 'A', 'Networking', 'Hard'),
        ('What is mDNS?', 'Multicast DNS for local networks', 'Master DNS', 'Mobile DNS', 'Managed DNS', 'A', 'Networking', 'Hard'),
        ('What is SR-IOV?', 'Hardware virtualization for NICs', 'Software routing', 'Firewall tech', 'DNS cache', 'A', 'Networking', 'Hard'),
        ('What is eBPF?', 'Kernel programmable networking', 'User-space app', 'Database query', 'Web framework', 'A', 'Networking', 'Hard'),
        ('What is QUIC?', 'UDP-based secure transport', 'TCP replacement', 'DNS protocol', 'Email standard', 'A', 'Networking', 'Hard'),
        ('What is segment routing?', 'Source-routed packets', 'Destination routing', 'Static routing', 'Dynamic routing', 'A', 'Networking', 'Hard'),
        ('What is NETCONF?', 'Network config protocol', 'File transfer', 'Email routing', 'Web standard', 'A', 'Networking', 'Hard'),
        ('What is intent-based networking?', 'Declare desired state', 'Manual config', 'Static routing', 'Firewall rules', 'A', 'Networking', 'Hard')
    ]
    
    c.executemany('''INSERT INTO questions 
                    (question, option_a, option_b, option_c, option_d, correct_answer, category, difficulty) 
                    VALUES (?,?,?,?,?,?,?,?)''', questions)
    
    # Demo users & results for leaderboard/profile
    demo_users = [
        ('Aarav Sharma', 'demo123', 'aarav@test.com', '2024-01-10'),
        ('Priya Singh', 'demo123', 'priya@test.com', '2024-01-12'),
        ('Rahul Verma', 'demo123', 'rahul@test.com', '2024-01-15'),
        ('Neha Gupta', 'demo123', 'neha@test.com', '2024-01-18'),
        ('Vikram Patel', 'demo123', 'vikram@test.com', '2024-01-20')
    ]
    c.executemany('INSERT INTO users (username, password, email, created_at) VALUES (?,?,?,?)', demo_users)
    
    demo_results = [
        (2, 7, 10, 'Python', 'Medium', 70.0, '2024-02-01 10:30', '245s'),
        (3, 9, 10, 'DBMS', 'Hard', 90.0, '2024-02-02 11:15', '310s'),
        (4, 6, 10, 'Web Dev', 'Easy', 60.0, '2024-02-03 09:45', '198s'),
        (5, 8, 10, 'Java', 'Medium', 80.0, '2024-02-04 14:20', '275s'),
        (2, 8, 10, 'Data Science', 'Hard', 80.0, '2024-02-05 16:00', '220s'),
        (3, 10, 10, 'Networking', 'Very Easy', 100.0, '2024-02-06 12:30', '350s'),
        (4, 7, 10, 'Python', 'Easy', 70.0, '2024-02-07 10:00', '210s'),
        (5, 9, 10, 'DBMS', 'Medium', 90.0, '2024-02-08 15:45', '290s'),
        (2, 6, 10, 'Web Dev', 'Hard', 60.0, '2024-02-09 11:20', '185s'),
        (3, 8, 10, 'Java', 'Very Easy', 80.0, '2024-02-10 13:10', '240s')
    ]
    c.executemany('''INSERT INTO results (user_id, score, total, category, difficulty, percentage, date, time_taken) 
                     VALUES (?,?,?,?,?,?,?,?)''', demo_results)
    
    conn.commit()
    conn.close()

# ============ ROUTES ============
@app.route('/')
def home():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    return render_template('index.html', page='login')

@app.route('/register', methods=['POST'])
def register():
    username, email, password = request.form['username'], request.form['email'], request.form['password']
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, email, created_at) VALUES (?,?,?,?)', 
              (username, password, email, datetime.now().strftime('%Y-%m-%d')))
    conn.commit()
    session['user_id'], session['username'] = c.lastrowid, username
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def login():
    email, password = request.form['email'], request.form['password']
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
    user = c.fetchone()
    conn.close()
    if user:
        session['user_id'], session['username'] = user[0], user[1]
        return redirect(url_for('dashboard'))
    return render_template('index.html', page='login', error='Invalid credentials!')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT score, total, category, difficulty, percentage, date, time_taken FROM results WHERE user_id=? ORDER BY date DESC LIMIT 10', (session['user_id'],))
    results = c.fetchall()
    conn.close()
    return render_template('index.html', page='dashboard', username=session['username'], results=results)

@app.route('/select-difficulty/<category>')
def select_difficulty(category):
    if 'user_id' not in session: return redirect(url_for('home'))
    return render_template('index.html', page='difficulty', category=category)

@app.route('/quiz')
def quiz():
    if 'user_id' not in session: return redirect(url_for('home'))
    category = request.args.get('category', 'All')
    difficulty = request.args.get('difficulty', 'All')
    
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    if category == 'All' and difficulty == 'All':
        c.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 10')
    elif category == 'All':
        c.execute('SELECT * FROM questions WHERE difficulty=? ORDER BY RANDOM() LIMIT 10', (difficulty,))
    elif difficulty == 'All':
        c.execute('SELECT * FROM questions WHERE category=? ORDER BY RANDOM() LIMIT 10', (category,))
    else:
        c.execute('SELECT * FROM questions WHERE category=? AND difficulty=? ORDER BY RANDOM() LIMIT 10', (category, difficulty))
    questions = c.fetchall()
    conn.close()
    return render_template('index.html', page='quiz', questions=questions, selected_category=category, selected_difficulty=difficulty)

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session: return redirect(url_for('home'))
    score = 0
    total = 10
    time_taken = request.form.get('time_taken', '0')
    category = request.form.get('category', 'All')
    difficulty = request.form.get('difficulty', 'All')
    
    for i in range(1, total + 1):
        if request.form.get(f'q{i}') == request.form.get(f'correct{i}'):
            score += 1
    percentage = (score / total) * 100
    
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''INSERT INTO results (user_id, score, total, category, difficulty, percentage, date, time_taken) 
                 VALUES (?,?,?,?,?,?,?,?)''', 
              (session['user_id'], score, total, category, difficulty, percentage, datetime.now().strftime('%Y-%m-%d %H:%M'), time_taken))
    result_id = c.lastrowid
    conn.commit()
    conn.close()
    return render_template('index.html', page='result', score=score, total=total, percentage=percentage, time_taken=time_taken, category=category, difficulty=difficulty, result_id=result_id)

@app.route('/profile')
def profile():
    if 'user_id' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''SELECT COUNT(*), AVG(percentage), MAX(percentage), SUM(CASE WHEN percentage >= 80 THEN 1 ELSE 0 END) FROM results WHERE user_id=?''', (session['user_id'],))
    stats = c.fetchone()
    c.execute('''SELECT category, difficulty, score, total, percentage, date FROM results WHERE user_id=? ORDER BY date DESC LIMIT 5''', (session['user_id'],))
    recent = c.fetchall()
    conn.close()
    return render_template('index.html', page='profile', stats=stats, recent=recent)

@app.route('/leaderboard')
def leaderboard():
    if 'user_id' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''SELECT u.username, COUNT(r.id) as attempts, AVG(r.percentage) as avg_score, MAX(r.percentage) as best_score
                 FROM users u JOIN results r ON u.id = r.user_id
                 GROUP BY u.id ORDER BY avg_score DESC, best_score DESC LIMIT 10''')
    leaders = c.fetchall()
    conn.close()
    return render_template('index.html', page='leaderboard', leaders=leaders)

@app.route('/study-materials')
def study_materials():
    if 'user_id' not in session: return redirect(url_for('home'))
    materials = {
        'Python': [{'title': 'Python Official Docs', 'type': 'PDF', 'link': 'https://docs.python.org/3/'}, {'title': 'Automate the Boring Stuff', 'type': 'Book', 'link': '#'}, {'title': 'Corey Schafer Tutorials', 'type': 'Video', 'link': 'https://youtube.com/c/Coreyms'}, {'title': 'HackerRank Python', 'type': 'Practice', 'link': 'https://hackerrank.com/domains/python'}],
        'Web Dev': [{'title': 'MDN Web Docs', 'type': 'Docs', 'link': 'https://developer.mozilla.org/'}, {'title': 'FreeCodeCamp', 'type': 'Course', 'link': 'https://freecodecamp.org'}, {'title': 'JavaScript.info', 'type': 'Article', 'link': 'https://javascript.info'}, {'title': 'Frontend Mentor', 'type': 'Practice', 'link': 'https://frontendmentor.io'}],
        'DBMS': [{'title': 'SQLZoo', 'type': 'Practice', 'link': 'https://sqlzoo.net'}, {'title': 'W3Schools SQL', 'type': 'Docs', 'link': 'https://w3schools.com/sql'}, {'title': 'Database System Concepts', 'type': 'Book', 'link': '#'}, {'title': 'LeetCode Database', 'type': 'Practice', 'link': 'https://leetcode.com/tag/database'}],
        'Java': [{'title': 'Oracle Java Docs', 'type': 'Docs', 'link': 'https://docs.oracle.com/javase/'}, {'title': 'Head First Java', 'type': 'Book', 'link': '#'}, {'title': 'Java Brains', 'type': 'Video', 'link': 'https://youtube.com/c/JavaBrains'}, {'title': 'HackerRank Java', 'type': 'Practice', 'link': 'https://hackerrank.com/domains/java'}],
        'Data Science': [{'title': 'Kaggle Learn', 'type': 'Course', 'link': 'https://kaggle.com/learn'}, {'title': 'Pandas Docs', 'type': 'Docs', 'link': 'https://pandas.pydata.org/docs/'}, {'title': 'Andrew Ng ML', 'type': 'Video', 'link': 'https://coursera.org/learn/machine-learning'}, {'title': 'DataCamp', 'type': 'Practice', 'link': 'https://datacamp.com'}],
        'Networking': [{'title': 'Cisco NetAcad', 'type': 'Course', 'link': 'https://netacad.com'}, {'title': 'Computer Networking: Top-Down', 'type': 'Book', 'link': '#'}, {'title': 'Professor Messer', 'type': 'Video', 'link': 'https://youtube.com/c/professormesser'}, {'title': 'Packet Tracer Labs', 'type': 'Practice', 'link': 'https://netacad.com/courses/packet-tracer'}]
    }
    return render_template('index.html', page='materials', materials=materials)

@app.route('/certificate/<int:result_id>')
def certificate(result_id):
    if 'user_id' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT * FROM results WHERE id=? AND user_id=?', (result_id, session['user_id']))
    result = c.fetchone()
    conn.close()
    if result and result[5] >= 80:
        return render_template('index.html', page='certificate', result=result, username=session['username'])
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)