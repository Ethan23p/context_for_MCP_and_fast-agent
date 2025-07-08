# Project: filesystem

## Directory Structure

```
📁 filesystem
├── 📁 __tests__
│   ├── 📄 path-utils.test.ts
│   ├── 📄 path-validation.test.ts
│   └── 📄 roots-utils.test.ts
├── 📄 Dockerfile
├── 📄 index.ts
├── 📄 jest.config.cjs
├── 📄 package.json
├── 📄 path-utils.ts
├── 📄 path-validation.ts
├── 📄 README.md
├── 📄 roots-utils.ts
└── 📄 tsconfig.json
```

------------------------------------------------------------

## File Contents

--- START OF FILE __tests__/path-utils.test.ts ---
import { describe, it, expect } from '@jest/globals';
import { normalizePath, expandHome, convertToWindowsPath } from '../path-utils.js';

describe('Path Utilities', () => {
  describe('convertToWindowsPath', () => {
    it('leaves Unix paths unchanged', () => {
      expect(convertToWindowsPath('/usr/local/bin'))
        .toBe('/usr/local/bin');
      expect(convertToWindowsPath('/home/user/some path'))
        .toBe('/home/user/some path');
    });

    it('converts WSL paths to Windows format', () => {
      expect(convertToWindowsPath('/mnt/c/NS/MyKindleContent'))
        .toBe('C:\\NS\\MyKindleContent');
    });

    it('converts Unix-style Windows paths to Windows format', () => {
      expect(convertToWindowsPath('/c/NS/MyKindleContent'))
        .toBe('C:\\NS\\MyKindleContent');
    });

    it('leaves Windows paths unchanged but ensures backslashes', () => {
      expect(convertToWindowsPath('C:\\NS\\MyKindleContent'))
        .toBe('C:\\NS\\MyKindleContent');
      expect(convertToWindowsPath('C:/NS/MyKindleContent'))
        .toBe('C:\\NS\\MyKindleContent');
    });

    it('handles Windows paths with spaces', () => {
      expect(convertToWindowsPath('C:\\Program Files\\Some App'))
        .toBe('C:\\Program Files\\Some App');
      expect(convertToWindowsPath('C:/Program Files/Some App'))
        .toBe('C:\\Program Files\\Some App');
    });

    it('handles uppercase and lowercase drive letters', () => {
      expect(convertToWindowsPath('/mnt/d/some/path'))
        .toBe('D:\\some\\path');
      expect(convertToWindowsPath('/d/some/path'))
        .toBe('D:\\some\\path');
    });
  });

  describe('normalizePath', () => {
    it('preserves Unix paths', () => {
      expect(normalizePath('/usr/local/bin'))
        .toBe('/usr/local/bin');
      expect(normalizePath('/home/user/some path'))
        .toBe('/home/user/some path');
      expect(normalizePath('"/usr/local/some app/"'))
        .toBe('/usr/local/some app');
    });

    it('removes surrounding quotes', () => {
      expect(normalizePath('"C:\\NS\\My Kindle Content"'))
        .toBe('C:\\NS\\My Kindle Content');
    });

    it('normalizes backslashes', () => {
      expect(normalizePath('C:\\\\NS\\\\MyKindleContent'))
        .toBe('C:\\NS\\MyKindleContent');
    });

    it('converts forward slashes to backslashes on Windows', () => {
      expect(normalizePath('C:/NS/MyKindleContent'))
        .toBe('C:\\NS\\MyKindleContent');
    });

    it('handles WSL paths', () => {
      expect(normalizePath('/mnt/c/NS/MyKindleContent'))
        .toBe('C:\\NS\\MyKindleContent');
    });

    it('handles Unix-style Windows paths', () => {
      expect(normalizePath('/c/NS/MyKindleContent'))
        .toBe('C:\\NS\\MyKindleContent');
    });

    it('handles paths with spaces and mixed slashes', () => {
      expect(normalizePath('C:/NS/My Kindle Content'))
        .toBe('C:\\NS\\My Kindle Content');
      expect(normalizePath('/mnt/c/NS/My Kindle Content'))
        .toBe('C:\\NS\\My Kindle Content');
      expect(normalizePath('C:\\Program Files (x86)\\App Name'))
        .toBe('C:\\Program Files (x86)\\App Name');
      expect(normalizePath('"C:\\Program Files\\App Name"'))
        .toBe('C:\\Program Files\\App Name');
      expect(normalizePath('  C:\\Program Files\\App Name  '))
        .toBe('C:\\Program Files\\App Name');
    });

    it('preserves spaces in all path formats', () => {
      expect(normalizePath('/mnt/c/Program Files/App Name'))
        .toBe('C:\\Program Files\\App Name');
      expect(normalizePath('/c/Program Files/App Name'))
        .toBe('C:\\Program Files\\App Name');
      expect(normalizePath('C:/Program Files/App Name'))
        .toBe('C:\\Program Files\\App Name');
    });

    it('handles special characters in paths', () => {
      // Test ampersand in path
      expect(normalizePath('C:\\NS\\Sub&Folder'))
        .toBe('C:\\NS\\Sub&Folder');
      expect(normalizePath('C:/NS/Sub&Folder'))
        .toBe('C:\\NS\\Sub&Folder');
      expect(normalizePath('/mnt/c/NS/Sub&Folder'))
        .toBe('C:\\NS\\Sub&Folder');
      
      // Test tilde in path (short names in Windows)
      expect(normalizePath('C:\\NS\\MYKIND~1'))
        .toBe('C:\\NS\\MYKIND~1');
      expect(normalizePath('/Users/NEMANS~1/FOLDER~2/SUBFO~1/Public/P12PST~1'))
        .toBe('/Users/NEMANS~1/FOLDER~2/SUBFO~1/Public/P12PST~1');
      
      // Test other special characters
      expect(normalizePath('C:\\Path with #hash'))
        .toBe('C:\\Path with #hash');
      expect(normalizePath('C:\\Path with (parentheses)'))
        .toBe('C:\\Path with (parentheses)');
      expect(normalizePath('C:\\Path with [brackets]'))
        .toBe('C:\\Path with [brackets]');
      expect(normalizePath('C:\\Path with @at+plus$dollar%percent'))
        .toBe('C:\\Path with @at+plus$dollar%percent');
    });

    it('capitalizes lowercase drive letters for Windows paths', () => {
      expect(normalizePath('c:/windows/system32'))
        .toBe('C:\\windows\\system32');
      expect(normalizePath('/mnt/d/my/folder')) // WSL path with lowercase drive
        .toBe('D:\\my\\folder');
      expect(normalizePath('/e/another/folder')) // Unix-style Windows path with lowercase drive
        .toBe('E:\\another\\folder');
    });

    it('handles UNC paths correctly', () => {
      // UNC paths should preserve the leading double backslash
      const uncPath = '\\\\SERVER\\share\\folder';
      expect(normalizePath(uncPath)).toBe('\\\\SERVER\\share\\folder');
      
      // Test UNC path with double backslashes that need normalization
      const uncPathWithDoubles = '\\\\\\\\SERVER\\\\share\\\\folder';
      expect(normalizePath(uncPathWithDoubles)).toBe('\\\\SERVER\\share\\folder');
    });

    it('returns normalized non-Windows/WSL/Unix-style Windows paths as is after basic normalization', () => {
      // Relative path
      const relativePath = 'some/relative/path';
      expect(normalizePath(relativePath)).toBe(relativePath.replace(/\//g, '\\'));

      // A path that looks somewhat absolute but isn't a drive or recognized Unix root for Windows conversion
      const otherAbsolutePath = '\\someserver\\share\\file';
      expect(normalizePath(otherAbsolutePath)).toBe(otherAbsolutePath);
    });
  });

  describe('expandHome', () => {
    it('expands ~ to home directory', () => {
      const result = expandHome('~/test');
      expect(result).toContain('test');
      expect(result).not.toContain('~');
    });

    it('leaves other paths unchanged', () => {
      expect(expandHome('C:/test')).toBe('C:/test');
    });
  });
});

--- END OF FILE __tests__/path-utils.test.ts ---


--- START OF FILE __tests__/path-validation.test.ts ---
import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import * as path from 'path';
import * as fs from 'fs/promises';
import * as os from 'os';
import { isPathWithinAllowedDirectories } from '../path-validation.js';

describe('Path Validation', () => {
  it('allows exact directory match', () => {
    const allowed = ['/home/user/project'];
    expect(isPathWithinAllowedDirectories('/home/user/project', allowed)).toBe(true);
  });

  it('allows subdirectories', () => {
    const allowed = ['/home/user/project'];
    expect(isPathWithinAllowedDirectories('/home/user/project/src', allowed)).toBe(true);
    expect(isPathWithinAllowedDirectories('/home/user/project/src/index.js', allowed)).toBe(true);
    expect(isPathWithinAllowedDirectories('/home/user/project/deeply/nested/file.txt', allowed)).toBe(true);
  });

  it('blocks similar directory names (prefix vulnerability)', () => {
    const allowed = ['/home/user/project'];
    expect(isPathWithinAllowedDirectories('/home/user/project2', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/home/user/project_backup', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/home/user/project-old', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/home/user/projectile', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/home/user/project.bak', allowed)).toBe(false);
  });

  it('blocks paths outside allowed directories', () => {
    const allowed = ['/home/user/project'];
    expect(isPathWithinAllowedDirectories('/home/user/other', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/etc/passwd', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/home/user', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/', allowed)).toBe(false);
  });

  it('handles multiple allowed directories', () => {
    const allowed = ['/home/user/project1', '/home/user/project2'];
    expect(isPathWithinAllowedDirectories('/home/user/project1/src', allowed)).toBe(true);
    expect(isPathWithinAllowedDirectories('/home/user/project2/src', allowed)).toBe(true);
    expect(isPathWithinAllowedDirectories('/home/user/project3', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/home/user/project1_backup', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/home/user/project2-old', allowed)).toBe(false);
  });

  it('blocks parent and sibling directories', () => {
    const allowed = ['/test/allowed'];

    // Parent directory
    expect(isPathWithinAllowedDirectories('/test', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/', allowed)).toBe(false);

    // Sibling with common prefix
    expect(isPathWithinAllowedDirectories('/test/allowed_sibling', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/test/allowed2', allowed)).toBe(false);
  });

  it('handles paths with special characters', () => {
    const allowed = ['/home/user/my-project (v2)'];

    expect(isPathWithinAllowedDirectories('/home/user/my-project (v2)', allowed)).toBe(true);
    expect(isPathWithinAllowedDirectories('/home/user/my-project (v2)/src', allowed)).toBe(true);
    expect(isPathWithinAllowedDirectories('/home/user/my-project (v2)_backup', allowed)).toBe(false);
    expect(isPathWithinAllowedDirectories('/home/user/my-project', allowed)).toBe(false);
  });

  describe('Input validation', () => {
    it('rejects empty inputs', () => {
      const allowed = ['/home/user/project'];

      expect(isPathWithinAllowedDirectories('', allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/project', [])).toBe(false);
    });

    it('handles trailing separators correctly', () => {
      const allowed = ['/home/user/project'];

      // Path with trailing separator should still match
      expect(isPathWithinAllowedDirectories('/home/user/project/', allowed)).toBe(true);

      // Allowed directory with trailing separator
      const allowedWithSep = ['/home/user/project/'];
      expect(isPathWithinAllowedDirectories('/home/user/project', allowedWithSep)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/project/', allowedWithSep)).toBe(true);

      // Should still block similar names with or without trailing separators
      expect(isPathWithinAllowedDirectories('/home/user/project2', allowedWithSep)).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/project2', allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/project2/', allowed)).toBe(false);
    });

    it('skips empty directory entries in allowed list', () => {
      const allowed = ['', '/home/user/project', ''];
      expect(isPathWithinAllowedDirectories('/home/user/project', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/project/src', allowed)).toBe(true);

      // Should still validate properly with empty entries
      expect(isPathWithinAllowedDirectories('/home/user/other', allowed)).toBe(false);
    });

    it('handles Windows paths with trailing separators', () => {
      if (path.sep === '\\') {
        const allowed = ['C:\\Users\\project'];

        // Path with trailing separator
        expect(isPathWithinAllowedDirectories('C:\\Users\\project\\', allowed)).toBe(true);

        // Allowed with trailing separator
        const allowedWithSep = ['C:\\Users\\project\\'];
        expect(isPathWithinAllowedDirectories('C:\\Users\\project', allowedWithSep)).toBe(true);
        expect(isPathWithinAllowedDirectories('C:\\Users\\project\\', allowedWithSep)).toBe(true);

        // Should still block similar names
        expect(isPathWithinAllowedDirectories('C:\\Users\\project2\\', allowed)).toBe(false);
      }
    });
  });

  describe('Error handling', () => {
    it('normalizes relative paths to absolute', () => {
      const allowed = [process.cwd()];

      // Relative paths get normalized to absolute paths based on cwd
      expect(isPathWithinAllowedDirectories('relative/path', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('./file', allowed)).toBe(true);

      // Parent directory references that escape allowed directory
      const parentAllowed = ['/home/user/project'];
      expect(isPathWithinAllowedDirectories('../parent', parentAllowed)).toBe(false);
    });

    it('returns false for relative paths in allowed directories', () => {
      const badAllowed = ['relative/path', '/some/other/absolute/path'];

      // Relative paths in allowed dirs are normalized to absolute based on cwd
      // The normalized 'relative/path' won't match our test path
      expect(isPathWithinAllowedDirectories('/some/other/absolute/path/file', badAllowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/absolute/path/file', badAllowed)).toBe(false);
    });

    it('handles null and undefined inputs gracefully', () => {
      const allowed = ['/home/user/project'];

      // Should return false, not crash
      expect(isPathWithinAllowedDirectories(null as any, allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories(undefined as any, allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('/path', null as any)).toBe(false);
      expect(isPathWithinAllowedDirectories('/path', undefined as any)).toBe(false);
    });
  });

  describe('Unicode and special characters', () => {
    it('handles unicode characters in paths', () => {
      const allowed = ['/home/user/café'];

      expect(isPathWithinAllowedDirectories('/home/user/café', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/café/file', allowed)).toBe(true);

      // Different unicode representation won't match (not normalized)
      const decomposed = '/home/user/cafe\u0301'; // e + combining accent
      expect(isPathWithinAllowedDirectories(decomposed, allowed)).toBe(false);
    });

    it('handles paths with spaces correctly', () => {
      const allowed = ['/home/user/my project'];

      expect(isPathWithinAllowedDirectories('/home/user/my project', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/my project/file', allowed)).toBe(true);

      // Partial matches should fail
      expect(isPathWithinAllowedDirectories('/home/user/my', allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/my proj', allowed)).toBe(false);
    });
  });

  describe('Overlapping allowed directories', () => {
    it('handles nested allowed directories correctly', () => {
      const allowed = ['/home', '/home/user', '/home/user/project'];

      // All paths under /home are allowed
      expect(isPathWithinAllowedDirectories('/home/anything', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/anything', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/project/anything', allowed)).toBe(true);

      // First match wins (most permissive)
      expect(isPathWithinAllowedDirectories('/home/other/deep/path', allowed)).toBe(true);
    });

    it('handles root directory as allowed', () => {
      const allowed = ['/'];

      // Everything is allowed under root (dangerous configuration)
      expect(isPathWithinAllowedDirectories('/', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/any/path', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/etc/passwd', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/secret', allowed)).toBe(true);

      // But only on the same filesystem root
      if (path.sep === '\\') {
        expect(isPathWithinAllowedDirectories('D:\\other', ['/'])).toBe(false);
      }
    });
  });

  describe('Cross-platform behavior', () => {
    it('handles Windows-style paths on Windows', () => {
      if (path.sep === '\\') {
        const allowed = ['C:\\Users\\project'];
        expect(isPathWithinAllowedDirectories('C:\\Users\\project', allowed)).toBe(true);
        expect(isPathWithinAllowedDirectories('C:\\Users\\project\\src', allowed)).toBe(true);
        expect(isPathWithinAllowedDirectories('C:\\Users\\project2', allowed)).toBe(false);
        expect(isPathWithinAllowedDirectories('C:\\Users\\project_backup', allowed)).toBe(false);
      }
    });

    it('handles Unix-style paths on Unix', () => {
      if (path.sep === '/') {
        const allowed = ['/home/user/project'];
        expect(isPathWithinAllowedDirectories('/home/user/project', allowed)).toBe(true);
        expect(isPathWithinAllowedDirectories('/home/user/project/src', allowed)).toBe(true);
        expect(isPathWithinAllowedDirectories('/home/user/project2', allowed)).toBe(false);
      }
    });
  });

  describe('Validation Tests - Path Traversal', () => {
    it('blocks path traversal attempts', () => {
      const allowed = ['/home/user/project'];

      // Basic traversal attempts
      expect(isPathWithinAllowedDirectories('/home/user/project/../../../etc/passwd', allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/project/../../other', allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/project/../project2', allowed)).toBe(false);

      // Mixed traversal with valid segments
      expect(isPathWithinAllowedDirectories('/home/user/project/src/../../project2', allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/project/./../../other', allowed)).toBe(false);

      // Multiple traversal sequences
      expect(isPathWithinAllowedDirectories('/home/user/project/../project/../../../etc', allowed)).toBe(false);
    });

    it('blocks traversal in allowed directories', () => {
      const allowed = ['/home/user/project/../safe'];

      // The allowed directory itself should be normalized and safe
      expect(isPathWithinAllowedDirectories('/home/user/safe/file', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/project/file', allowed)).toBe(false);
    });

    it('handles complex traversal patterns', () => {
      const allowed = ['/home/user/project'];

      // Double dots in filenames (not traversal) - these normalize to paths within allowed dir
      expect(isPathWithinAllowedDirectories('/home/user/project/..test', allowed)).toBe(true); // Not traversal
      expect(isPathWithinAllowedDirectories('/home/user/project/test..', allowed)).toBe(true); // Not traversal
      expect(isPathWithinAllowedDirectories('/home/user/project/te..st', allowed)).toBe(true); // Not traversal

      // Actual traversal
      expect(isPathWithinAllowedDirectories('/home/user/project/../test', allowed)).toBe(false); // Is traversal - goes to /home/user/test

      // Edge case: /home/user/project/.. normalizes to /home/user (parent dir)
      expect(isPathWithinAllowedDirectories('/home/user/project/..', allowed)).toBe(false); // Goes to parent
    });
  });

  describe('Validation Tests - Null Bytes', () => {
    it('rejects paths with null bytes', () => {
      const allowed = ['/home/user/project'];

      expect(isPathWithinAllowedDirectories('/home/user/project\x00/etc/passwd', allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/project/test\x00.txt', allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('\x00/home/user/project', allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/project/\x00', allowed)).toBe(false);
    });

    it('rejects allowed directories with null bytes', () => {
      const allowed = ['/home/user/project\x00'];

      expect(isPathWithinAllowedDirectories('/home/user/project', allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/project/file', allowed)).toBe(false);
    });
  });

  describe('Validation Tests - Special Characters', () => {
    it('allows percent signs in filenames', () => {
      const allowed = ['/home/user/project'];

      // Percent is a valid filename character
      expect(isPathWithinAllowedDirectories('/home/user/project/report_50%.pdf', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/project/Q1_25%_growth', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/project/%41', allowed)).toBe(true); // File named %41

      // URL encoding is NOT decoded by path.normalize, so these are just odd filenames
      expect(isPathWithinAllowedDirectories('/home/user/project/%2e%2e', allowed)).toBe(true); // File named "%2e%2e"
      expect(isPathWithinAllowedDirectories('/home/user/project/file%20name', allowed)).toBe(true); // File with %20 in name
    });

    it('handles percent signs in allowed directories', () => {
      const allowed = ['/home/user/project%20files'];

      // This is a directory literally named "project%20files"
      expect(isPathWithinAllowedDirectories('/home/user/project%20files/test', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/project files/test', allowed)).toBe(false); // Different dir
    });
  });

  describe('Path Normalization', () => {
    it('normalizes paths before comparison', () => {
      const allowed = ['/home/user/project'];

      // Trailing slashes
      expect(isPathWithinAllowedDirectories('/home/user/project/', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/project//', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/project///', allowed)).toBe(true);

      // Current directory references
      expect(isPathWithinAllowedDirectories('/home/user/project/./src', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/./project/src', allowed)).toBe(true);

      // Multiple slashes
      expect(isPathWithinAllowedDirectories('/home/user/project//src//file', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home//user//project//src', allowed)).toBe(true);

      // Should still block outside paths
      expect(isPathWithinAllowedDirectories('/home/user//project2', allowed)).toBe(false);
    });

    it('handles mixed separators correctly', () => {
      if (path.sep === '\\') {
        const allowed = ['C:\\Users\\project'];

        // Mixed separators should be normalized
        expect(isPathWithinAllowedDirectories('C:/Users/project', allowed)).toBe(true);
        expect(isPathWithinAllowedDirectories('C:\\Users/project\\src', allowed)).toBe(true);
        expect(isPathWithinAllowedDirectories('C:/Users\\project/src', allowed)).toBe(true);
      }
    });
  });

  describe('Edge Cases', () => {
    it('rejects non-string inputs safely', () => {
      const allowed = ['/home/user/project'];

      expect(isPathWithinAllowedDirectories(123 as any, allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories({} as any, allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories([] as any, allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories(null as any, allowed)).toBe(false);
      expect(isPathWithinAllowedDirectories(undefined as any, allowed)).toBe(false);

      // Non-string in allowed directories
      expect(isPathWithinAllowedDirectories('/home/user/project', [123 as any])).toBe(false);
      expect(isPathWithinAllowedDirectories('/home/user/project', [{} as any])).toBe(false);
    });

    it('handles very long paths', () => {
      const allowed = ['/home/user/project'];

      // Create a very long path that's still valid
      const longSubPath = 'a/'.repeat(1000) + 'file.txt';
      expect(isPathWithinAllowedDirectories(`/home/user/project/${longSubPath}`, allowed)).toBe(true);

      // Very long path that escapes
      const escapePath = 'a/'.repeat(1000) + '../'.repeat(1001) + 'etc/passwd';
      expect(isPathWithinAllowedDirectories(`/home/user/project/${escapePath}`, allowed)).toBe(false);
    });
  });

  describe('Additional Coverage', () => {
    it('handles allowed directories with traversal that normalizes safely', () => {
      // These allowed dirs contain traversal but normalize to valid paths
      const allowed = ['/home/user/../user/project'];

      // Should normalize to /home/user/project and work correctly
      expect(isPathWithinAllowedDirectories('/home/user/project/file', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/other', allowed)).toBe(false);
    });

    it('handles symbolic dots in filenames', () => {
      const allowed = ['/home/user/project'];

      // Single and double dots as actual filenames (not traversal)
      expect(isPathWithinAllowedDirectories('/home/user/project/.', allowed)).toBe(true);
      expect(isPathWithinAllowedDirectories('/home/user/project/..', allowed)).toBe(false); // This normalizes to parent
      expect(isPathWithinAllowedDirectories('/home/user/project/...', allowed)).toBe(true); // Three dots is a valid filename
      expect(isPathWithinAllowedDirectories('/home/user/project/....', allowed)).toBe(true); // Four dots is a valid filename
    });

    it('handles UNC paths on Windows', () => {
      if (path.sep === '\\') {
        const allowed = ['\\\\server\\share\\project'];

        expect(isPathWithinAllowedDirectories('\\\\server\\share\\project', allowed)).toBe(true);
        expect(isPathWithinAllowedDirectories('\\\\server\\share\\project\\file', allowed)).toBe(true);
        expect(isPathWithinAllowedDirectories('\\\\server\\share\\other', allowed)).toBe(false);
        expect(isPathWithinAllowedDirectories('\\\\other\\share\\project', allowed)).toBe(false);
      }
    });
  });

  describe('Symlink Tests', () => {
    let testDir: string;
    let allowedDir: string;
    let forbiddenDir: string;

    beforeEach(async () => {
      testDir = await fs.mkdtemp(path.join(os.tmpdir(), 'fs-error-test-'));
      allowedDir = path.join(testDir, 'allowed');
      forbiddenDir = path.join(testDir, 'forbidden');

      await fs.mkdir(allowedDir, { recursive: true });
      await fs.mkdir(forbiddenDir, { recursive: true });
    });

    afterEach(async () => {
      await fs.rm(testDir, { recursive: true, force: true });
    });

    it('validates symlink handling', async () => {
      // Test with symlinks
      try {
        const linkPath = path.join(allowedDir, 'bad-link');
        const targetPath = path.join(forbiddenDir, 'target.txt');

        await fs.writeFile(targetPath, 'content');
        await fs.symlink(targetPath, linkPath);

        // In real implementation, this would throw with the resolved path
        const realPath = await fs.realpath(linkPath);
        const allowed = [allowedDir];

        // Symlink target should be outside allowed directory
        expect(isPathWithinAllowedDirectories(realPath, allowed)).toBe(false);
      } catch (error) {
        // Skip if no symlink permissions
      }
    });

    it('handles non-existent paths correctly', async () => {
      const newFilePath = path.join(allowedDir, 'subdir', 'newfile.txt');

      // Parent directory doesn't exist
      try {
        await fs.access(newFilePath);
      } catch (error) {
        expect((error as NodeJS.ErrnoException).code).toBe('ENOENT');
      }

      // After creating parent, validation should work
      await fs.mkdir(path.dirname(newFilePath), { recursive: true });
      const allowed = [allowedDir];
      expect(isPathWithinAllowedDirectories(newFilePath, allowed)).toBe(true);
    });

    // Test path resolution consistency for symlinked files
    it('validates symlinked files consistently between path and resolved forms', async () => {
      try {
        // Setup: Create target file in forbidden area
        const targetFile = path.join(forbiddenDir, 'target.txt');
        await fs.writeFile(targetFile, 'TARGET_CONTENT');

        // Create symlink inside allowed directory pointing to forbidden file
        const symlinkPath = path.join(allowedDir, 'link-to-target.txt');
        await fs.symlink(targetFile, symlinkPath);

        // The symlink path itself passes validation (looks like it's in allowed dir)
        expect(isPathWithinAllowedDirectories(symlinkPath, [allowedDir])).toBe(true);

        // But the resolved path should fail validation
        const resolvedPath = await fs.realpath(symlinkPath);
        expect(isPathWithinAllowedDirectories(resolvedPath, [allowedDir])).toBe(false);

        // Verify the resolved path goes to the forbidden location (normalize both paths for macOS temp dirs)
        expect(await fs.realpath(resolvedPath)).toBe(await fs.realpath(targetFile));
      } catch (error) {
        // Skip if no symlink permissions on the system
        if ((error as NodeJS.ErrnoException).code !== 'EPERM') {
          throw error;
        }
      }
    });

    // Test allowed directory resolution behavior
    it('validates paths correctly when allowed directory is resolved from symlink', async () => {
      try {
        // Setup: Create the actual target directory with content
        const actualTargetDir = path.join(testDir, 'actual-target');
        await fs.mkdir(actualTargetDir, { recursive: true });
        const targetFile = path.join(actualTargetDir, 'file.txt');
        await fs.writeFile(targetFile, 'FILE_CONTENT');

        // Setup: Create symlink directory that points to target
        const symlinkDir = path.join(testDir, 'symlink-dir');
        await fs.symlink(actualTargetDir, symlinkDir);

        // Simulate resolved allowed directory (what the server startup should do)
        const resolvedAllowedDir = await fs.realpath(symlinkDir);
        const resolvedTargetDir = await fs.realpath(actualTargetDir);
        expect(resolvedAllowedDir).toBe(resolvedTargetDir);

        // Test 1: File access through original symlink path should pass validation with resolved allowed dir
        const fileViaSymlink = path.join(symlinkDir, 'file.txt');
        const resolvedFile = await fs.realpath(fileViaSymlink);
        expect(isPathWithinAllowedDirectories(resolvedFile, [resolvedAllowedDir])).toBe(true);

        // Test 2: File access through resolved path should also pass validation
        const fileViaResolved = path.join(resolvedTargetDir, 'file.txt');
        expect(isPathWithinAllowedDirectories(fileViaResolved, [resolvedAllowedDir])).toBe(true);

        // Test 3: Demonstrate inconsistent behavior with unresolved allowed directories
        // If allowed dirs were not resolved (storing symlink paths instead):
        const unresolvedAllowedDirs = [symlinkDir];
        // This validation would incorrectly fail for the same content:
        expect(isPathWithinAllowedDirectories(resolvedFile, unresolvedAllowedDirs)).toBe(false);

      } catch (error) {
        // Skip if no symlink permissions on the system
        if ((error as NodeJS.ErrnoException).code !== 'EPERM') {
          throw error;
        }
      }
    });

    it('resolves nested symlink chains completely', async () => {
      try {
        // Setup: Create target file in forbidden area
        const actualTarget = path.join(forbiddenDir, 'target-file.txt');
        await fs.writeFile(actualTarget, 'FINAL_CONTENT');

        // Create chain of symlinks: allowedFile -> link2 -> link1 -> actualTarget
        const link1 = path.join(testDir, 'intermediate-link1');
        const link2 = path.join(testDir, 'intermediate-link2');
        const allowedFile = path.join(allowedDir, 'seemingly-safe-file');

        await fs.symlink(actualTarget, link1);
        await fs.symlink(link1, link2);
        await fs.symlink(link2, allowedFile);

        // The allowed file path passes basic validation
        expect(isPathWithinAllowedDirectories(allowedFile, [allowedDir])).toBe(true);

        // But complete resolution reveals the forbidden target
        const fullyResolvedPath = await fs.realpath(allowedFile);
        expect(isPathWithinAllowedDirectories(fullyResolvedPath, [allowedDir])).toBe(false);
        expect(await fs.realpath(fullyResolvedPath)).toBe(await fs.realpath(actualTarget));

      } catch (error) {
        // Skip if no symlink permissions on the system
        if ((error as NodeJS.ErrnoException).code !== 'EPERM') {
          throw error;
        }
      }
    });
  });

  describe('Path Validation Race Condition Tests', () => {
    let testDir: string;
    let allowedDir: string;
    let forbiddenDir: string;
    let targetFile: string;
    let testPath: string;

    beforeEach(async () => {
      testDir = await fs.mkdtemp(path.join(os.tmpdir(), 'race-test-'));
      allowedDir = path.join(testDir, 'allowed');
      forbiddenDir = path.join(testDir, 'outside');
      targetFile = path.join(forbiddenDir, 'target.txt');
      testPath = path.join(allowedDir, 'test.txt');

      await fs.mkdir(allowedDir, { recursive: true });
      await fs.mkdir(forbiddenDir, { recursive: true });
      await fs.writeFile(targetFile, 'ORIGINAL CONTENT', 'utf-8');
    });

    afterEach(async () => {
      await fs.rm(testDir, { recursive: true, force: true });
    });

    it('validates non-existent file paths based on parent directory', async () => {
      const allowed = [allowedDir];

      expect(isPathWithinAllowedDirectories(testPath, allowed)).toBe(true);
      await expect(fs.access(testPath)).rejects.toThrow();

      const parentDir = path.dirname(testPath);
      expect(isPathWithinAllowedDirectories(parentDir, allowed)).toBe(true);
    });

    it('demonstrates symlink race condition allows writing outside allowed directories', async () => {
      const allowed = [allowedDir];

      await expect(fs.access(testPath)).rejects.toThrow();
      expect(isPathWithinAllowedDirectories(testPath, allowed)).toBe(true);

      await fs.symlink(targetFile, testPath);
      await fs.writeFile(testPath, 'MODIFIED CONTENT', 'utf-8');

      const targetContent = await fs.readFile(targetFile, 'utf-8');
      expect(targetContent).toBe('MODIFIED CONTENT');

      const resolvedPath = await fs.realpath(testPath);
      expect(isPathWithinAllowedDirectories(resolvedPath, allowed)).toBe(false);
    });

    it('shows timing differences between validation approaches', async () => {
      const allowed = [allowedDir];

      const validation1 = isPathWithinAllowedDirectories(testPath, allowed);
      expect(validation1).toBe(true);

      await fs.symlink(targetFile, testPath);

      const resolvedPath = await fs.realpath(testPath);
      const validation2 = isPathWithinAllowedDirectories(resolvedPath, allowed);
      expect(validation2).toBe(false);

      expect(validation1).not.toBe(validation2);
    });

    it('validates directory creation timing', async () => {
      const allowed = [allowedDir];
      const testDir = path.join(allowedDir, 'newdir');

      expect(isPathWithinAllowedDirectories(testDir, allowed)).toBe(true);

      await fs.symlink(forbiddenDir, testDir);

      expect(isPathWithinAllowedDirectories(testDir, allowed)).toBe(true);

      const resolved = await fs.realpath(testDir);
      expect(isPathWithinAllowedDirectories(resolved, allowed)).toBe(false);
    });

    it('demonstrates exclusive file creation behavior', async () => {
      const allowed = [allowedDir];

      await fs.symlink(targetFile, testPath);

      await expect(fs.open(testPath, 'wx')).rejects.toThrow(/EEXIST/);

      await fs.writeFile(testPath, 'NEW CONTENT', 'utf-8');
      const targetContent = await fs.readFile(targetFile, 'utf-8');
      expect(targetContent).toBe('NEW CONTENT');
    });

    it('should use resolved parent paths for non-existent files', async () => {
      const allowed = [allowedDir];

      const symlinkDir = path.join(allowedDir, 'link');
      await fs.symlink(forbiddenDir, symlinkDir);

      const fileThroughSymlink = path.join(symlinkDir, 'newfile.txt');

      expect(fileThroughSymlink.startsWith(allowedDir)).toBe(true);

      const parentDir = path.dirname(fileThroughSymlink);
      const resolvedParent = await fs.realpath(parentDir);
      expect(isPathWithinAllowedDirectories(resolvedParent, allowed)).toBe(false);

      const expectedSafePath = path.join(resolvedParent, path.basename(fileThroughSymlink));
      expect(isPathWithinAllowedDirectories(expectedSafePath, allowed)).toBe(false);
    });

    it('demonstrates parent directory symlink traversal', async () => {
      const allowed = [allowedDir];
      const deepPath = path.join(allowedDir, 'sub1', 'sub2', 'file.txt');

      expect(isPathWithinAllowedDirectories(deepPath, allowed)).toBe(true);

      const sub1Path = path.join(allowedDir, 'sub1');
      await fs.symlink(forbiddenDir, sub1Path);

      await fs.mkdir(path.join(sub1Path, 'sub2'), { recursive: true });
      await fs.writeFile(deepPath, 'CONTENT', 'utf-8');

      const realPath = await fs.realpath(deepPath);
      const realAllowedDir = await fs.realpath(allowedDir);
      const realForbiddenDir = await fs.realpath(forbiddenDir);

      expect(realPath.startsWith(realAllowedDir)).toBe(false);
      expect(realPath.startsWith(realForbiddenDir)).toBe(true);
    });

    it('should prevent race condition between validatePath and file operation', async () => {
      const allowed = [allowedDir];
      const racePath = path.join(allowedDir, 'race-file.txt');
      const targetFile = path.join(forbiddenDir, 'target.txt');

      await fs.writeFile(targetFile, 'ORIGINAL CONTENT', 'utf-8');

      // Path validation would pass (file doesn't exist, parent is in allowed dir)
      expect(await fs.access(racePath).then(() => false).catch(() => true)).toBe(true);
      expect(isPathWithinAllowedDirectories(racePath, allowed)).toBe(true);

      // Race condition: symlink created after validation but before write
      await fs.symlink(targetFile, racePath);

      // With exclusive write flag, write should fail on symlink
      await expect(
        fs.writeFile(racePath, 'NEW CONTENT', { encoding: 'utf-8', flag: 'wx' })
      ).rejects.toThrow(/EEXIST/);

      // Verify content unchanged
      const targetContent = await fs.readFile(targetFile, 'utf-8');
      expect(targetContent).toBe('ORIGINAL CONTENT');

      // The symlink exists but write was blocked
      const actualWritePath = await fs.realpath(racePath);
      expect(actualWritePath).toBe(await fs.realpath(targetFile));
      expect(isPathWithinAllowedDirectories(actualWritePath, allowed)).toBe(false);
    });

    it('should allow overwrites to legitimate files within allowed directories', async () => {
      const allowed = [allowedDir];
      const legitFile = path.join(allowedDir, 'legit-file.txt');

      // Create a legitimate file
      await fs.writeFile(legitFile, 'ORIGINAL', 'utf-8');

      // Opening with w should work for legitimate files
      const fd = await fs.open(legitFile, 'w');
      try {
        await fd.write('UPDATED', 0, 'utf-8');
      } finally {
        await fd.close();
      }

      const content = await fs.readFile(legitFile, 'utf-8');
      expect(content).toBe('UPDATED');
    });

    it('should handle symlinks that point within allowed directories', async () => {
      const allowed = [allowedDir];
      const targetFile = path.join(allowedDir, 'target.txt');
      const symlinkPath = path.join(allowedDir, 'symlink.txt');

      // Create target file within allowed directory
      await fs.writeFile(targetFile, 'TARGET CONTENT', 'utf-8');

      // Create symlink pointing to allowed file
      await fs.symlink(targetFile, symlinkPath);

      // Opening symlink with w follows it to the target
      const fd = await fs.open(symlinkPath, 'w');
      try {
        await fd.write('UPDATED VIA SYMLINK', 0, 'utf-8');
      } finally {
        await fd.close();
      }

      // Both symlink and target should show updated content
      const symlinkContent = await fs.readFile(symlinkPath, 'utf-8');
      const targetContent = await fs.readFile(targetFile, 'utf-8');
      expect(symlinkContent).toBe('UPDATED VIA SYMLINK');
      expect(targetContent).toBe('UPDATED VIA SYMLINK');
    });

    it('should prevent overwriting files through symlinks pointing outside allowed directories', async () => {
      const allowed = [allowedDir];
      const legitFile = path.join(allowedDir, 'existing.txt');
      const targetFile = path.join(forbiddenDir, 'target.txt');

      // Create a legitimate file first
      await fs.writeFile(legitFile, 'LEGIT CONTENT', 'utf-8');

      // Create target file in forbidden directory
      await fs.writeFile(targetFile, 'FORBIDDEN CONTENT', 'utf-8');

      // Now replace the legitimate file with a symlink to forbidden location
      await fs.unlink(legitFile);
      await fs.symlink(targetFile, legitFile);

      // Simulate the server's validation logic
      const stats = await fs.lstat(legitFile);
      expect(stats.isSymbolicLink()).toBe(true);

      const realPath = await fs.realpath(legitFile);
      expect(isPathWithinAllowedDirectories(realPath, allowed)).toBe(false);

      // With atomic rename, symlinks are replaced not followed
      // So this test now demonstrates the protection

      // Verify content remains unchanged
      const targetContent = await fs.readFile(targetFile, 'utf-8');
      expect(targetContent).toBe('FORBIDDEN CONTENT');
    });

    it('demonstrates race condition in read operations', async () => {
      const allowed = [allowedDir];
      const legitFile = path.join(allowedDir, 'readable.txt');
      const secretFile = path.join(forbiddenDir, 'secret.txt');

      // Create legitimate file
      await fs.writeFile(legitFile, 'PUBLIC CONTENT', 'utf-8');

      // Create secret file in forbidden directory
      await fs.writeFile(secretFile, 'SECRET CONTENT', 'utf-8');

      // Step 1: validatePath would pass for legitimate file
      expect(isPathWithinAllowedDirectories(legitFile, allowed)).toBe(true);

      // Step 2: Race condition - replace file with symlink after validation
      await fs.unlink(legitFile);
      await fs.symlink(secretFile, legitFile);

      // Step 3: Read operation follows symlink to forbidden location
      const content = await fs.readFile(legitFile, 'utf-8');

      // This shows the vulnerability - we read forbidden content
      expect(content).toBe('SECRET CONTENT');
      expect(isPathWithinAllowedDirectories(await fs.realpath(legitFile), allowed)).toBe(false);
    });

    it('verifies rename does not follow symlinks', async () => {
      const allowed = [allowedDir];
      const tempFile = path.join(allowedDir, 'temp.txt');
      const targetSymlink = path.join(allowedDir, 'target-symlink.txt');
      const forbiddenTarget = path.join(forbiddenDir, 'forbidden-target.txt');

      // Create forbidden target
      await fs.writeFile(forbiddenTarget, 'ORIGINAL CONTENT', 'utf-8');

      // Create symlink pointing to forbidden location
      await fs.symlink(forbiddenTarget, targetSymlink);

      // Write temp file
      await fs.writeFile(tempFile, 'NEW CONTENT', 'utf-8');

      // Rename temp file to symlink path
      await fs.rename(tempFile, targetSymlink);

      // Check what happened
      const symlinkExists = await fs.lstat(targetSymlink).then(() => true).catch(() => false);
      const isSymlink = symlinkExists && (await fs.lstat(targetSymlink)).isSymbolicLink();
      const targetContent = await fs.readFile(targetSymlink, 'utf-8');
      const forbiddenContent = await fs.readFile(forbiddenTarget, 'utf-8');

      // Rename should replace the symlink with a regular file
      expect(isSymlink).toBe(false);
      expect(targetContent).toBe('NEW CONTENT');
      expect(forbiddenContent).toBe('ORIGINAL CONTENT'); // Unchanged
    });
  });
});

--- END OF FILE __tests__/path-validation.test.ts ---


--- START OF FILE __tests__/roots-utils.test.ts ---
import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { getValidRootDirectories } from '../roots-utils.js';
import { mkdtempSync, rmSync, mkdirSync, writeFileSync, realpathSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';
import type { Root } from '@modelcontextprotocol/sdk/types.js';

describe('getValidRootDirectories', () => {
  let testDir1: string;
  let testDir2: string;
  let testDir3: string;
  let testFile: string;

  beforeEach(() => {
    // Create test directories
    testDir1 = realpathSync(mkdtempSync(join(tmpdir(), 'mcp-roots-test1-')));
    testDir2 = realpathSync(mkdtempSync(join(tmpdir(), 'mcp-roots-test2-')));
    testDir3 = realpathSync(mkdtempSync(join(tmpdir(), 'mcp-roots-test3-')));

    // Create a test file (not a directory)
    testFile = join(testDir1, 'test-file.txt');
    writeFileSync(testFile, 'test content');
  });

  afterEach(() => {
    // Cleanup
    rmSync(testDir1, { recursive: true, force: true });
    rmSync(testDir2, { recursive: true, force: true });
    rmSync(testDir3, { recursive: true, force: true });
  });

  describe('valid directory processing', () => {
    it('should process all URI formats and edge cases', async () => {
      const roots = [
        { uri: `file://${testDir1}`, name: 'File URI' },
        { uri: testDir2, name: 'Plain path' },
        { uri: testDir3 } // Plain path without name property
      ];

      const result = await getValidRootDirectories(roots);

      expect(result).toContain(testDir1);
      expect(result).toContain(testDir2);
      expect(result).toContain(testDir3);
      expect(result).toHaveLength(3);
    });

    it('should normalize complex paths', async () => {
      const subDir = join(testDir1, 'subdir');
      mkdirSync(subDir);
      
      const roots = [
        { uri: `file://${testDir1}/./subdir/../subdir`, name: 'Complex Path' }
      ];

      const result = await getValidRootDirectories(roots);

      expect(result).toHaveLength(1);
      expect(result[0]).toBe(subDir);
    });
  });

  describe('error handling', () => {

    it('should handle various error types', async () => {
      const nonExistentDir = join(tmpdir(), 'non-existent-directory-12345');
      const invalidPath = '\0invalid\0path'; // Null bytes cause different error types
      const roots = [
        { uri: `file://${testDir1}`, name: 'Valid Dir' },
        { uri: `file://${nonExistentDir}`, name: 'Non-existent Dir' },
        { uri: `file://${testFile}`, name: 'File Not Dir' },
        { uri: `file://${invalidPath}`, name: 'Invalid Path' }
      ];

      const result = await getValidRootDirectories(roots);

      expect(result).toContain(testDir1);
      expect(result).not.toContain(nonExistentDir);
      expect(result).not.toContain(testFile);
      expect(result).not.toContain(invalidPath);
      expect(result).toHaveLength(1);
    });
  });
});
--- END OF FILE __tests__/roots-utils.test.ts ---


--- START OF FILE Dockerfile ---
FROM node:22.12-alpine AS builder

WORKDIR /app

COPY src/filesystem /app
COPY tsconfig.json /tsconfig.json

RUN --mount=type=cache,target=/root/.npm npm install

RUN --mount=type=cache,target=/root/.npm-production npm ci --ignore-scripts --omit-dev


FROM node:22-alpine AS release

WORKDIR /app

COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/package.json /app/package.json
COPY --from=builder /app/package-lock.json /app/package-lock.json

ENV NODE_ENV=production

RUN npm ci --ignore-scripts --omit-dev

ENTRYPOINT ["node", "/app/dist/index.js"]
--- END OF FILE Dockerfile ---


--- START OF FILE index.ts ---
#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ToolSchema,
  RootsListChangedNotificationSchema,
  type Root,
} from "@modelcontextprotocol/sdk/types.js";
import fs from "fs/promises";
import path from "path";
import os from 'os';
import { randomBytes } from 'crypto';
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";
import { diffLines, createTwoFilesPatch } from 'diff';
import { minimatch } from 'minimatch';
import { isPathWithinAllowedDirectories } from './path-validation.js';
import { getValidRootDirectories } from './roots-utils.js';

// Command line argument parsing
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error("Usage: mcp-server-filesystem [allowed-directory] [additional-directories...]");
  console.error("Note: Allowed directories can be provided via:");
  console.error("  1. Command-line arguments (shown above)");
  console.error("  2. MCP roots protocol (if client supports it)");
  console.error("At least one directory must be provided by EITHER method for the server to operate.");
}

// Normalize all paths consistently
function normalizePath(p: string): string {
  return path.normalize(p);
}

function expandHome(filepath: string): string {
  if (filepath.startsWith('~/') || filepath === '~') {
    return path.join(os.homedir(), filepath.slice(1));
  }
  return filepath;
}

// Store allowed directories in normalized and resolved form
let allowedDirectories = await Promise.all(
  args.map(async (dir) => {
    const expanded = expandHome(dir);
    const absolute = path.resolve(expanded);
    try {
      // Resolve symlinks in allowed directories during startup
      const resolved = await fs.realpath(absolute);
      return normalizePath(resolved);
    } catch (error) {
      // If we can't resolve (doesn't exist), use the normalized absolute path
      // This allows configuring allowed dirs that will be created later
      return normalizePath(absolute);
    }
  })
);

// Validate that all directories exist and are accessible
await Promise.all(args.map(async (dir) => {
  try {
    const stats = await fs.stat(expandHome(dir));
    if (!stats.isDirectory()) {
      console.error(`Error: ${dir} is not a directory`);
      process.exit(1);
    }
  } catch (error) {
    console.error(`Error accessing directory ${dir}:`, error);
    process.exit(1);
  }
}));

// Security utilities
async function validatePath(requestedPath: string): Promise<string> {
  const expandedPath = expandHome(requestedPath);
  const absolute = path.isAbsolute(expandedPath)
    ? path.resolve(expandedPath)
    : path.resolve(process.cwd(), expandedPath);

  const normalizedRequested = normalizePath(absolute);

  // Check if path is within allowed directories
  const isAllowed = isPathWithinAllowedDirectories(normalizedRequested, allowedDirectories);
  if (!isAllowed) {
    throw new Error(`Access denied - path outside allowed directories: ${absolute} not in ${allowedDirectories.join(', ')}`);
  }

  // Handle symlinks by checking their real path
  try {
    const realPath = await fs.realpath(absolute);
    const normalizedReal = normalizePath(realPath);
    if (!isPathWithinAllowedDirectories(normalizedReal, allowedDirectories)) {
      throw new Error(`Access denied - symlink target outside allowed directories: ${realPath} not in ${allowedDirectories.join(', ')}`);
    }
    return realPath;
  } catch (error) {
    // For new files that don't exist yet, verify parent directory
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      const parentDir = path.dirname(absolute);
      try {
        const realParentPath = await fs.realpath(parentDir);
        const normalizedParent = normalizePath(realParentPath);
        if (!isPathWithinAllowedDirectories(normalizedParent, allowedDirectories)) {
          throw new Error(`Access denied - parent directory outside allowed directories: ${realParentPath} not in ${allowedDirectories.join(', ')}`);
        }
        return absolute;
      } catch {
        throw new Error(`Parent directory does not exist: ${parentDir}`);
      }
    }
    throw error;
  }
}

// Schema definitions
const ReadFileArgsSchema = z.object({
  path: z.string(),
  tail: z.number().optional().describe('If provided, returns only the last N lines of the file'),
  head: z.number().optional().describe('If provided, returns only the first N lines of the file')
});

const ReadMultipleFilesArgsSchema = z.object({
  paths: z.array(z.string()),
});

const WriteFileArgsSchema = z.object({
  path: z.string(),
  content: z.string(),
});

const EditOperation = z.object({
  oldText: z.string().describe('Text to search for - must match exactly'),
  newText: z.string().describe('Text to replace with')
});

const EditFileArgsSchema = z.object({
  path: z.string(),
  edits: z.array(EditOperation),
  dryRun: z.boolean().default(false).describe('Preview changes using git-style diff format')
});

const CreateDirectoryArgsSchema = z.object({
  path: z.string(),
});

const ListDirectoryArgsSchema = z.object({
  path: z.string(),
});

const ListDirectoryWithSizesArgsSchema = z.object({
  path: z.string(),
  sortBy: z.enum(['name', 'size']).optional().default('name').describe('Sort entries by name or size'),
});

const DirectoryTreeArgsSchema = z.object({
  path: z.string(),
});

const MoveFileArgsSchema = z.object({
  source: z.string(),
  destination: z.string(),
});

const SearchFilesArgsSchema = z.object({
  path: z.string(),
  pattern: z.string(),
  excludePatterns: z.array(z.string()).optional().default([])
});

const GetFileInfoArgsSchema = z.object({
  path: z.string(),
});

const ToolInputSchema = ToolSchema.shape.inputSchema;
type ToolInput = z.infer<typeof ToolInputSchema>;

interface FileInfo {
  size: number;
  created: Date;
  modified: Date;
  accessed: Date;
  isDirectory: boolean;
  isFile: boolean;
  permissions: string;
}

// Server setup
const server = new Server(
  {
    name: "secure-filesystem-server",
    version: "0.2.0",
  },
  {
    capabilities: {
      tools: {},
    },
  },
);

// Tool implementations
async function getFileStats(filePath: string): Promise<FileInfo> {
  const stats = await fs.stat(filePath);
  return {
    size: stats.size,
    created: stats.birthtime,
    modified: stats.mtime,
    accessed: stats.atime,
    isDirectory: stats.isDirectory(),
    isFile: stats.isFile(),
    permissions: stats.mode.toString(8).slice(-3),
  };
}

async function searchFiles(
  rootPath: string,
  pattern: string,
  excludePatterns: string[] = []
): Promise<string[]> {
  const results: string[] = [];

  async function search(currentPath: string) {
    const entries = await fs.readdir(currentPath, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);

      try {
        // Validate each path before processing
        await validatePath(fullPath);

        // Check if path matches any exclude pattern
        const relativePath = path.relative(rootPath, fullPath);
        const shouldExclude = excludePatterns.some(pattern => {
          const globPattern = pattern.includes('*') ? pattern : `**/${pattern}/**`;
          return minimatch(relativePath, globPattern, { dot: true });
        });

        if (shouldExclude) {
          continue;
        }

        if (entry.name.toLowerCase().includes(pattern.toLowerCase())) {
          results.push(fullPath);
        }

        if (entry.isDirectory()) {
          await search(fullPath);
        }
      } catch (error) {
        // Skip invalid paths during search
        continue;
      }
    }
  }

  await search(rootPath);
  return results;
}

// file editing and diffing utilities
function normalizeLineEndings(text: string): string {
  return text.replace(/\r\n/g, '\n');
}

function createUnifiedDiff(originalContent: string, newContent: string, filepath: string = 'file'): string {
  // Ensure consistent line endings for diff
  const normalizedOriginal = normalizeLineEndings(originalContent);
  const normalizedNew = normalizeLineEndings(newContent);

  return createTwoFilesPatch(
    filepath,
    filepath,
    normalizedOriginal,
    normalizedNew,
    'original',
    'modified'
  );
}

async function applyFileEdits(
  filePath: string,
  edits: Array<{oldText: string, newText: string}>,
  dryRun = false
): Promise<string> {
  // Read file content and normalize line endings
  const content = normalizeLineEndings(await fs.readFile(filePath, 'utf-8'));

  // Apply edits sequentially
  let modifiedContent = content;
  for (const edit of edits) {
    const normalizedOld = normalizeLineEndings(edit.oldText);
    const normalizedNew = normalizeLineEndings(edit.newText);

    // If exact match exists, use it
    if (modifiedContent.includes(normalizedOld)) {
      modifiedContent = modifiedContent.replace(normalizedOld, normalizedNew);
      continue;
    }

    // Otherwise, try line-by-line matching with flexibility for whitespace
    const oldLines = normalizedOld.split('\n');
    const contentLines = modifiedContent.split('\n');
    let matchFound = false;

    for (let i = 0; i <= contentLines.length - oldLines.length; i++) {
      const potentialMatch = contentLines.slice(i, i + oldLines.length);

      // Compare lines with normalized whitespace
      const isMatch = oldLines.every((oldLine, j) => {
        const contentLine = potentialMatch[j];
        return oldLine.trim() === contentLine.trim();
      });

      if (isMatch) {
        // Preserve original indentation of first line
        const originalIndent = contentLines[i].match(/^\s*/)?.[0] || '';
        const newLines = normalizedNew.split('\n').map((line, j) => {
          if (j === 0) return originalIndent + line.trimStart();
          // For subsequent lines, try to preserve relative indentation
          const oldIndent = oldLines[j]?.match(/^\s*/)?.[0] || '';
          const newIndent = line.match(/^\s*/)?.[0] || '';
          if (oldIndent && newIndent) {
            const relativeIndent = newIndent.length - oldIndent.length;
            return originalIndent + ' '.repeat(Math.max(0, relativeIndent)) + line.trimStart();
          }
          return line;
        });

        contentLines.splice(i, oldLines.length, ...newLines);
        modifiedContent = contentLines.join('\n');
        matchFound = true;
        break;
      }
    }

    if (!matchFound) {
      throw new Error(`Could not find exact match for edit:\n${edit.oldText}`);
    }
  }

  // Create unified diff
  const diff = createUnifiedDiff(content, modifiedContent, filePath);

  // Format diff with appropriate number of backticks
  let numBackticks = 3;
  while (diff.includes('`'.repeat(numBackticks))) {
    numBackticks++;
  }
  const formattedDiff = `${'`'.repeat(numBackticks)}diff\n${diff}${'`'.repeat(numBackticks)}\n\n`;

  if (!dryRun) {
    // Security: Use atomic rename to prevent race conditions where symlinks
    // could be created between validation and write. Rename operations
    // replace the target file atomically and don't follow symlinks.
    const tempPath = `${filePath}.${randomBytes(16).toString('hex')}.tmp`;
    try {
      await fs.writeFile(tempPath, modifiedContent, 'utf-8');
      await fs.rename(tempPath, filePath);
    } catch (error) {
      try {
        await fs.unlink(tempPath);
      } catch {}
      throw error;
    }
  }

  return formattedDiff;
}

// Helper functions
function formatSize(bytes: number): string {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  if (bytes === 0) return '0 B';
  
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  if (i === 0) return `${bytes} ${units[i]}`;
  
  return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${units[i]}`;
}

// Memory-efficient implementation to get the last N lines of a file
async function tailFile(filePath: string, numLines: number): Promise<string> {
  const CHUNK_SIZE = 1024; // Read 1KB at a time
  const stats = await fs.stat(filePath);
  const fileSize = stats.size;
  
  if (fileSize === 0) return '';
  
  // Open file for reading
  const fileHandle = await fs.open(filePath, 'r');
  try {
    const lines: string[] = [];
    let position = fileSize;
    let chunk = Buffer.alloc(CHUNK_SIZE);
    let linesFound = 0;
    let remainingText = '';
    
    // Read chunks from the end of the file until we have enough lines
    while (position > 0 && linesFound < numLines) {
      const size = Math.min(CHUNK_SIZE, position);
      position -= size;
      
      const { bytesRead } = await fileHandle.read(chunk, 0, size, position);
      if (!bytesRead) break;
      
      // Get the chunk as a string and prepend any remaining text from previous iteration
      const readData = chunk.slice(0, bytesRead).toString('utf-8');
      const chunkText = readData + remainingText;
      
      // Split by newlines and count
      const chunkLines = normalizeLineEndings(chunkText).split('\n');
      
      // If this isn't the end of the file, the first line is likely incomplete
      // Save it to prepend to the next chunk
      if (position > 0) {
        remainingText = chunkLines[0];
        chunkLines.shift(); // Remove the first (incomplete) line
      }
      
      // Add lines to our result (up to the number we need)
      for (let i = chunkLines.length - 1; i >= 0 && linesFound < numLines; i--) {
        lines.unshift(chunkLines[i]);
        linesFound++;
      }
    }
    
    return lines.join('\n');
  } finally {
    await fileHandle.close();
  }
}

// New function to get the first N lines of a file
async function headFile(filePath: string, numLines: number): Promise<string> {
  const fileHandle = await fs.open(filePath, 'r');
  try {
    const lines: string[] = [];
    let buffer = '';
    let bytesRead = 0;
    const chunk = Buffer.alloc(1024); // 1KB buffer
    
    // Read chunks and count lines until we have enough or reach EOF
    while (lines.length < numLines) {
      const result = await fileHandle.read(chunk, 0, chunk.length, bytesRead);
      if (result.bytesRead === 0) break; // End of file
      bytesRead += result.bytesRead;
      buffer += chunk.slice(0, result.bytesRead).toString('utf-8');
      
      const newLineIndex = buffer.lastIndexOf('\n');
      if (newLineIndex !== -1) {
        const completeLines = buffer.slice(0, newLineIndex).split('\n');
        buffer = buffer.slice(newLineIndex + 1);
        for (const line of completeLines) {
          lines.push(line);
          if (lines.length >= numLines) break;
        }
      }
    }
    
    // If there is leftover content and we still need lines, add it
    if (buffer.length > 0 && lines.length < numLines) {
      lines.push(buffer);
    }
    
    return lines.join('\n');
  } finally {
    await fileHandle.close();
  }
}

// Tool handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "read_file",
        description:
          "Read the complete contents of a file from the file system. " +
          "Handles various text encodings and provides detailed error messages " +
          "if the file cannot be read. Use this tool when you need to examine " +
          "the contents of a single file. Use the 'head' parameter to read only " +
          "the first N lines of a file, or the 'tail' parameter to read only " +
          "the last N lines of a file. Only works within allowed directories.",
        inputSchema: zodToJsonSchema(ReadFileArgsSchema) as ToolInput,
      },
      {
        name: "read_multiple_files",
        description:
          "Read the contents of multiple files simultaneously. This is more " +
          "efficient than reading files one by one when you need to analyze " +
          "or compare multiple files. Each file's content is returned with its " +
          "path as a reference. Failed reads for individual files won't stop " +
          "the entire operation. Only works within allowed directories.",
        inputSchema: zodToJsonSchema(ReadMultipleFilesArgsSchema) as ToolInput,
      },
      {
        name: "write_file",
        description:
          "Create a new file or completely overwrite an existing file with new content. " +
          "Use with caution as it will overwrite existing files without warning. " +
          "Handles text content with proper encoding. Only works within allowed directories.",
        inputSchema: zodToJsonSchema(WriteFileArgsSchema) as ToolInput,
      },
      {
        name: "edit_file",
        description:
          "Make line-based edits to a text file. Each edit replaces exact line sequences " +
          "with new content. Returns a git-style diff showing the changes made. " +
          "Only works within allowed directories.",
        inputSchema: zodToJsonSchema(EditFileArgsSchema) as ToolInput,
      },
      {
        name: "create_directory",
        description:
          "Create a new directory or ensure a directory exists. Can create multiple " +
          "nested directories in one operation. If the directory already exists, " +
          "this operation will succeed silently. Perfect for setting up directory " +
          "structures for projects or ensuring required paths exist. Only works within allowed directories.",
        inputSchema: zodToJsonSchema(CreateDirectoryArgsSchema) as ToolInput,
      },
      {
        name: "list_directory",
        description:
          "Get a detailed listing of all files and directories in a specified path. " +
          "Results clearly distinguish between files and directories with [FILE] and [DIR] " +
          "prefixes. This tool is essential for understanding directory structure and " +
          "finding specific files within a directory. Only works within allowed directories.",
        inputSchema: zodToJsonSchema(ListDirectoryArgsSchema) as ToolInput,
      },
      {
        name: "list_directory_with_sizes",
        description:
          "Get a detailed listing of all files and directories in a specified path, including sizes. " +
          "Results clearly distinguish between files and directories with [FILE] and [DIR] " +
          "prefixes. This tool is useful for understanding directory structure and " +
          "finding specific files within a directory. Only works within allowed directories.",
        inputSchema: zodToJsonSchema(ListDirectoryWithSizesArgsSchema) as ToolInput,
      },
      {
        name: "directory_tree",
        description:
            "Get a recursive tree view of files and directories as a JSON structure. " +
            "Each entry includes 'name', 'type' (file/directory), and 'children' for directories. " +
            "Files have no children array, while directories always have a children array (which may be empty). " +
            "The output is formatted with 2-space indentation for readability. Only works within allowed directories.",
        inputSchema: zodToJsonSchema(DirectoryTreeArgsSchema) as ToolInput,
      },
      {
        name: "move_file",
        description:
          "Move or rename files and directories. Can move files between directories " +
          "and rename them in a single operation. If the destination exists, the " +
          "operation will fail. Works across different directories and can be used " +
          "for simple renaming within the same directory. Both source and destination must be within allowed directories.",
        inputSchema: zodToJsonSchema(MoveFileArgsSchema) as ToolInput,
      },
      {
        name: "search_files",
        description:
          "Recursively search for files and directories matching a pattern. " +
          "Searches through all subdirectories from the starting path. The search " +
          "is case-insensitive and matches partial names. Returns full paths to all " +
          "matching items. Great for finding files when you don't know their exact location. " +
          "Only searches within allowed directories.",
        inputSchema: zodToJsonSchema(SearchFilesArgsSchema) as ToolInput,
      },
      {
        name: "get_file_info",
        description:
          "Retrieve detailed metadata about a file or directory. Returns comprehensive " +
          "information including size, creation time, last modified time, permissions, " +
          "and type. This tool is perfect for understanding file characteristics " +
          "without reading the actual content. Only works within allowed directories.",
        inputSchema: zodToJsonSchema(GetFileInfoArgsSchema) as ToolInput,
      },
      {
        name: "list_allowed_directories",
        description:
          "Returns the list of root directories that this server is allowed to access. " +
          "Use this to understand which directories are available before trying to access files. ",
        inputSchema: {
          type: "object",
          properties: {},
          required: [],
        },
      },
    ],
  };
});


server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const { name, arguments: args } = request.params;

    switch (name) {
      case "read_file": {
        const parsed = ReadFileArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for read_file: ${parsed.error}`);
        }
        const validPath = await validatePath(parsed.data.path);
        
        if (parsed.data.head && parsed.data.tail) {
          throw new Error("Cannot specify both head and tail parameters simultaneously");
        }
        
        if (parsed.data.tail) {
          // Use memory-efficient tail implementation for large files
          const tailContent = await tailFile(validPath, parsed.data.tail);
          return {
            content: [{ type: "text", text: tailContent }],
          };
        }
        
        if (parsed.data.head) {
          // Use memory-efficient head implementation for large files
          const headContent = await headFile(validPath, parsed.data.head);
          return {
            content: [{ type: "text", text: headContent }],
          };
        }
        
        const content = await fs.readFile(validPath, "utf-8");
        return {
          content: [{ type: "text", text: content }],
        };
      }

      case "read_multiple_files": {
        const parsed = ReadMultipleFilesArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for read_multiple_files: ${parsed.error}`);
        }
        const results = await Promise.all(
          parsed.data.paths.map(async (filePath: string) => {
            try {
              const validPath = await validatePath(filePath);
              const content = await fs.readFile(validPath, "utf-8");
              return `${filePath}:\n${content}\n`;
            } catch (error) {
              const errorMessage = error instanceof Error ? error.message : String(error);
              return `${filePath}: Error - ${errorMessage}`;
            }
          }),
        );
        return {
          content: [{ type: "text", text: results.join("\n---\n") }],
        };
      }

      case "write_file": {
        const parsed = WriteFileArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for write_file: ${parsed.error}`);
        }
        const validPath = await validatePath(parsed.data.path);

        try {
          // Security: 'wx' flag ensures exclusive creation - fails if file/symlink exists,
          // preventing writes through pre-existing symlinks
          await fs.writeFile(validPath, parsed.data.content, { encoding: "utf-8", flag: 'wx' });
        } catch (error) {
          if ((error as NodeJS.ErrnoException).code === 'EEXIST') {
            // Security: Use atomic rename to prevent race conditions where symlinks
            // could be created between validation and write. Rename operations
            // replace the target file atomically and don't follow symlinks.
            const tempPath = `${validPath}.${randomBytes(16).toString('hex')}.tmp`;
            try {
              await fs.writeFile(tempPath, parsed.data.content, 'utf-8');
              await fs.rename(tempPath, validPath);
            } catch (renameError) {
              try {
                await fs.unlink(tempPath);
              } catch {}
              throw renameError;
            }
          } else {
            throw error;
          }
        }

        return {
          content: [{ type: "text", text: `Successfully wrote to ${parsed.data.path}` }],
        };
      }

      case "edit_file": {
        const parsed = EditFileArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for edit_file: ${parsed.error}`);
        }
        const validPath = await validatePath(parsed.data.path);
        const result = await applyFileEdits(validPath, parsed.data.edits, parsed.data.dryRun);
        return {
          content: [{ type: "text", text: result }],
        };
      }

      case "create_directory": {
        const parsed = CreateDirectoryArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for create_directory: ${parsed.error}`);
        }
        const validPath = await validatePath(parsed.data.path);
        await fs.mkdir(validPath, { recursive: true });
        return {
          content: [{ type: "text", text: `Successfully created directory ${parsed.data.path}` }],
        };
      }

      case "list_directory": {
        const parsed = ListDirectoryArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for list_directory: ${parsed.error}`);
        }
        const validPath = await validatePath(parsed.data.path);
        const entries = await fs.readdir(validPath, { withFileTypes: true });
        const formatted = entries
          .map((entry) => `${entry.isDirectory() ? "[DIR]" : "[FILE]"} ${entry.name}`)
          .join("\n");
        return {
          content: [{ type: "text", text: formatted }],
        };
      }

      case "list_directory_with_sizes": {
        const parsed = ListDirectoryWithSizesArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for list_directory_with_sizes: ${parsed.error}`);
        }
        const validPath = await validatePath(parsed.data.path);
        const entries = await fs.readdir(validPath, { withFileTypes: true });
        
        // Get detailed information for each entry
        const detailedEntries = await Promise.all(
          entries.map(async (entry) => {
            const entryPath = path.join(validPath, entry.name);
            try {
              const stats = await fs.stat(entryPath);
              return {
                name: entry.name,
                isDirectory: entry.isDirectory(),
                size: stats.size,
                mtime: stats.mtime
              };
            } catch (error) {
              return {
                name: entry.name,
                isDirectory: entry.isDirectory(),
                size: 0,
                mtime: new Date(0)
              };
            }
          })
        );
        
        // Sort entries based on sortBy parameter
        const sortedEntries = [...detailedEntries].sort((a, b) => {
          if (parsed.data.sortBy === 'size') {
            return b.size - a.size; // Descending by size
          }
          // Default sort by name
          return a.name.localeCompare(b.name);
        });
        
        // Format the output
        const formattedEntries = sortedEntries.map(entry => 
          `${entry.isDirectory ? "[DIR]" : "[FILE]"} ${entry.name.padEnd(30)} ${
            entry.isDirectory ? "" : formatSize(entry.size).padStart(10)
          }`
        );
        
        // Add summary
        const totalFiles = detailedEntries.filter(e => !e.isDirectory).length;
        const totalDirs = detailedEntries.filter(e => e.isDirectory).length;
        const totalSize = detailedEntries.reduce((sum, entry) => sum + (entry.isDirectory ? 0 : entry.size), 0);
        
        const summary = [
          "",
          `Total: ${totalFiles} files, ${totalDirs} directories`,
          `Combined size: ${formatSize(totalSize)}`
        ];
        
        return {
          content: [{ 
            type: "text", 
            text: [...formattedEntries, ...summary].join("\n") 
          }],
        };
      }

      case "directory_tree": {
        const parsed = DirectoryTreeArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for directory_tree: ${parsed.error}`);
        }

            interface TreeEntry {
                name: string;
                type: 'file' | 'directory';
                children?: TreeEntry[];
            }

            async function buildTree(currentPath: string): Promise<TreeEntry[]> {
                const validPath = await validatePath(currentPath);
                const entries = await fs.readdir(validPath, {withFileTypes: true});
                const result: TreeEntry[] = [];

                for (const entry of entries) {
                    const entryData: TreeEntry = {
                        name: entry.name,
                        type: entry.isDirectory() ? 'directory' : 'file'
                    };

                    if (entry.isDirectory()) {
                        const subPath = path.join(currentPath, entry.name);
                        entryData.children = await buildTree(subPath);
                    }

                    result.push(entryData);
                }

                return result;
            }

            const treeData = await buildTree(parsed.data.path);
            return {
                content: [{
                    type: "text",
                    text: JSON.stringify(treeData, null, 2)
                }],
            };
        }

      case "move_file": {
        const parsed = MoveFileArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for move_file: ${parsed.error}`);
        }
        const validSourcePath = await validatePath(parsed.data.source);
        const validDestPath = await validatePath(parsed.data.destination);
        await fs.rename(validSourcePath, validDestPath);
        return {
          content: [{ type: "text", text: `Successfully moved ${parsed.data.source} to ${parsed.data.destination}` }],
        };
      }

      case "search_files": {
        const parsed = SearchFilesArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for search_files: ${parsed.error}`);
        }
        const validPath = await validatePath(parsed.data.path);
        const results = await searchFiles(validPath, parsed.data.pattern, parsed.data.excludePatterns);
        return {
          content: [{ type: "text", text: results.length > 0 ? results.join("\n") : "No matches found" }],
        };
      }

      case "get_file_info": {
        const parsed = GetFileInfoArgsSchema.safeParse(args);
        if (!parsed.success) {
          throw new Error(`Invalid arguments for get_file_info: ${parsed.error}`);
        }
        const validPath = await validatePath(parsed.data.path);
        const info = await getFileStats(validPath);
        return {
          content: [{ type: "text", text: Object.entries(info)
            .map(([key, value]) => `${key}: ${value}`)
            .join("\n") }],
        };
      }

      case "list_allowed_directories": {
        return {
          content: [{
            type: "text",
            text: `Allowed directories:\n${allowedDirectories.join('\n')}`
          }],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return {
      content: [{ type: "text", text: `Error: ${errorMessage}` }],
      isError: true,
    };
  }
});

// Updates allowed directories based on MCP client roots
async function updateAllowedDirectoriesFromRoots(requestedRoots: Root[]) {
  const validatedRootDirs = await getValidRootDirectories(requestedRoots);
  if (validatedRootDirs.length > 0) {
    allowedDirectories = [...validatedRootDirs];
    console.error(`Updated allowed directories from MCP roots: ${validatedRootDirs.length} valid directories`);
  } else {
    console.error("No valid root directories provided by client");
  }
}

// Handles dynamic roots updates during runtime, when client sends "roots/list_changed" notification, server fetches the updated roots and replaces all allowed directories with the new roots.
server.setNotificationHandler(RootsListChangedNotificationSchema, async () => {
  try {
    // Request the updated roots list from the client
    const response = await server.listRoots();
    if (response && 'roots' in response) {
      await updateAllowedDirectoriesFromRoots(response.roots);
    }
  } catch (error) {
    console.error("Failed to request roots from client:", error instanceof Error ? error.message : String(error));
  }
});

// Handles post-initialization setup, specifically checking for and fetching MCP roots.
server.oninitialized = async () => {
  const clientCapabilities = server.getClientCapabilities();

  if (clientCapabilities?.roots) {
    try {
      const response = await server.listRoots();
      if (response && 'roots' in response) {
        await updateAllowedDirectoriesFromRoots(response.roots);
      } else {
        console.error("Client returned no roots set, keeping current settings");
      }
    } catch (error) {
      console.error("Failed to request initial roots from client:", error instanceof Error ? error.message : String(error));
    }
  } else {
    if (allowedDirectories.length > 0) {
      console.error("Client does not support MCP Roots, using allowed directories set from server args:", allowedDirectories);
    }else{
      throw new Error(`Server cannot operate: No allowed directories available. Server was started without command-line directories and client either does not support MCP roots protocol or provided empty roots. Please either: 1) Start server with directory arguments, or 2) Use a client that supports MCP roots protocol and provides valid root directories.`);
    }
  }
};

// Start server
async function runServer() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Secure MCP Filesystem Server running on stdio");
  if (allowedDirectories.length === 0) {
    console.error("Started without allowed directories - waiting for client to provide roots via MCP protocol");
  }
}

runServer().catch((error) => {
  console.error("Fatal error running server:", error);
  process.exit(1);
});

--- END OF FILE index.ts ---


--- START OF FILE jest.config.cjs ---
/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  extensionsToTreatAsEsm: ['.ts'],
  moduleNameMapper: {
    '^(\\.{1,2}/.*)\\.js$': '$1',
  },
  transform: {
    '^.+\\.tsx?$': [
      'ts-jest',
      {
        useESM: true,
      },
    ],
  },
  testMatch: ['**/__tests__/**/*.test.ts'],
  collectCoverageFrom: [
    '**/*.ts',
    '!**/__tests__/**',
    '!**/dist/**',
  ],
}

--- END OF FILE jest.config.cjs ---


--- START OF FILE package.json ---
{
  "name": "@modelcontextprotocol/server-filesystem",
  "version": "0.6.2",
  "description": "MCP server for filesystem access",
  "license": "MIT",
  "author": "Anthropic, PBC (https://anthropic.com)",
  "homepage": "https://modelcontextprotocol.io",
  "bugs": "https://github.com/modelcontextprotocol/servers/issues",
  "type": "module",
  "bin": {
    "mcp-server-filesystem": "dist/index.js"
  },
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "tsc && shx chmod +x dist/*.js",
    "prepare": "npm run build",
    "watch": "tsc --watch",
    "test": "jest --config=jest.config.cjs --coverage"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.12.3",
    "diff": "^5.1.0",
    "glob": "^10.3.10",
    "minimatch": "^10.0.1",
    "zod-to-json-schema": "^3.23.5"
  },
  "devDependencies": {
    "@jest/globals": "^29.7.0",
    "@types/diff": "^5.0.9",
    "@types/jest": "^29.5.14",
    "@types/minimatch": "^5.1.2",
    "@types/node": "^22",
    "jest": "^29.7.0",
    "shx": "^0.3.4",
    "ts-jest": "^29.1.1",
    "ts-node": "^10.9.2",
    "typescript": "^5.8.2"
  }
}
--- END OF FILE package.json ---


--- START OF FILE path-utils.ts ---
import path from "path";
import os from 'os';

/**
 * Converts WSL or Unix-style Windows paths to Windows format
 * @param p The path to convert
 * @returns Converted Windows path
 */
export function convertToWindowsPath(p: string): string {
  // Handle WSL paths (/mnt/c/...)
  if (p.startsWith('/mnt/')) {
    const driveLetter = p.charAt(5).toUpperCase();
    const pathPart = p.slice(6).replace(/\//g, '\\');
    return `${driveLetter}:${pathPart}`;
  }
  
  // Handle Unix-style Windows paths (/c/...)
  if (p.match(/^\/[a-zA-Z]\//)) {
    const driveLetter = p.charAt(1).toUpperCase();
    const pathPart = p.slice(2).replace(/\//g, '\\');
    return `${driveLetter}:${pathPart}`;
  }

  // Handle standard Windows paths, ensuring backslashes
  if (p.match(/^[a-zA-Z]:/)) {
    return p.replace(/\//g, '\\');
  }

  // Leave non-Windows paths unchanged
  return p;
}

/**
 * Normalizes path by standardizing format while preserving OS-specific behavior
 * @param p The path to normalize
 * @returns Normalized path
 */
export function normalizePath(p: string): string {
  // Remove any surrounding quotes and whitespace
  p = p.trim().replace(/^["']|["']$/g, '');
  
  // Check if this is a Unix path (starts with / but not a Windows or WSL path)
  const isUnixPath = p.startsWith('/') && 
                    !p.match(/^\/mnt\/[a-z]\//i) && 
                    !p.match(/^\/[a-zA-Z]\//);
  
  if (isUnixPath) {
    // For Unix paths, just normalize without converting to Windows format
    // Replace double slashes with single slashes and remove trailing slashes
    return p.replace(/\/+/g, '/').replace(/\/+$/, '');
  }
  
  // Convert WSL or Unix-style Windows paths to Windows format
  p = convertToWindowsPath(p);
  
  // Handle double backslashes, preserving leading UNC \\
  if (p.startsWith('\\\\')) {
    // For UNC paths, first normalize any excessive leading backslashes to exactly \\
    // Then normalize double backslashes in the rest of the path
    let uncPath = p;
    // Replace multiple leading backslashes with exactly two
    uncPath = uncPath.replace(/^\\{2,}/, '\\\\');
    // Now normalize any remaining double backslashes in the rest of the path
    const restOfPath = uncPath.substring(2).replace(/\\\\/g, '\\');
    p = '\\\\' + restOfPath;
  } else {
    // For non-UNC paths, normalize all double backslashes
    p = p.replace(/\\\\/g, '\\');
  }
  
  // Use Node's path normalization, which handles . and .. segments
  let normalized = path.normalize(p);
  
  // Fix UNC paths after normalization (path.normalize can remove a leading backslash)
  if (p.startsWith('\\\\') && !normalized.startsWith('\\\\')) {
    normalized = '\\' + normalized;
  }
  
  // Handle Windows paths: convert slashes and ensure drive letter is capitalized
  if (normalized.match(/^[a-zA-Z]:/)) {
    let result = normalized.replace(/\//g, '\\');
    // Capitalize drive letter if present
    if (/^[a-z]:/.test(result)) {
      result = result.charAt(0).toUpperCase() + result.slice(1);
    }
    return result;
  }
  
  // For all other paths (including relative paths), convert forward slashes to backslashes
  // This ensures relative paths like "some/relative/path" become "some\\relative\\path"
  return normalized.replace(/\//g, '\\');
}

/**
 * Expands home directory tildes in paths
 * @param filepath The path to expand
 * @returns Expanded path
 */
export function expandHome(filepath: string): string {
  if (filepath.startsWith('~/') || filepath === '~') {
    return path.join(os.homedir(), filepath.slice(1));
  }
  return filepath;
}

--- END OF FILE path-utils.ts ---


--- START OF FILE path-validation.ts ---
import path from 'path';

/**
 * Checks if an absolute path is within any of the allowed directories.
 * 
 * @param absolutePath - The absolute path to check (will be normalized)
 * @param allowedDirectories - Array of absolute allowed directory paths (will be normalized)
 * @returns true if the path is within an allowed directory, false otherwise
 * @throws Error if given relative paths after normalization
 */
export function isPathWithinAllowedDirectories(absolutePath: string, allowedDirectories: string[]): boolean {
  // Type validation
  if (typeof absolutePath !== 'string' || !Array.isArray(allowedDirectories)) {
    return false;
  }

  // Reject empty inputs
  if (!absolutePath || allowedDirectories.length === 0) {
    return false;
  }

  // Reject null bytes (forbidden in paths)
  if (absolutePath.includes('\x00')) {
    return false;
  }

  // Normalize the input path
  let normalizedPath: string;
  try {
    normalizedPath = path.resolve(path.normalize(absolutePath));
  } catch {
    return false;
  }

  // Verify it's absolute after normalization
  if (!path.isAbsolute(normalizedPath)) {
    throw new Error('Path must be absolute after normalization');
  }

  // Check against each allowed directory
  return allowedDirectories.some(dir => {
    if (typeof dir !== 'string' || !dir) {
      return false;
    }

    // Reject null bytes in allowed dirs
    if (dir.includes('\x00')) {
      return false;
    }

    // Normalize the allowed directory
    let normalizedDir: string;
    try {
      normalizedDir = path.resolve(path.normalize(dir));
    } catch {
      return false;
    }

    // Verify allowed directory is absolute after normalization
    if (!path.isAbsolute(normalizedDir)) {
      throw new Error('Allowed directories must be absolute paths after normalization');
    }

    // Check if normalizedPath is within normalizedDir
    // Path is inside if it's the same or a subdirectory
    if (normalizedPath === normalizedDir) {
      return true;
    }
    
    // Special case for root directory to avoid double slash
    if (normalizedDir === path.sep) {
      return normalizedPath.startsWith(path.sep);
    }
    
    return normalizedPath.startsWith(normalizedDir + path.sep);
  });
}
--- END OF FILE path-validation.ts ---


--- START OF FILE README.md ---
# Filesystem MCP Server

Node.js server implementing Model Context Protocol (MCP) for filesystem operations.

## Features

- Read/write files
- Create/list/delete directories
- Move files/directories
- Search files
- Get file metadata
- Dynamic directory access control via [Roots](https://modelcontextprotocol.io/docs/concepts/roots)

## Directory Access Control

The server uses a flexible directory access control system. Directories can be specified via command-line arguments or dynamically via [Roots](https://modelcontextprotocol.io/docs/concepts/roots).

### Method 1: Command-line Arguments
Specify Allowed directories when starting the server:
```bash
mcp-server-filesystem /path/to/dir1 /path/to/dir2
```

### Method 2: MCP Roots (Recommended)
MCP clients that support [Roots](https://modelcontextprotocol.io/docs/concepts/roots) can dynamically update the Allowed directories. 

Roots notified by Client to Server, completely replace any server-side Allowed directories when provided.

**Important**: If server starts without command-line arguments AND client doesn't support roots protocol (or provides empty roots), the server will throw an error during initialization.

This is the recommended method, as this enables runtime directory updates via `roots/list_changed` notifications without server restart, providing a more flexible and modern integration experience.

### How It Works

The server's directory access control follows this flow:

1. **Server Startup**
   - Server starts with directories from command-line arguments (if provided)
   - If no arguments provided, server starts with empty allowed directories

2. **Client Connection & Initialization**
   - Client connects and sends `initialize` request with capabilities
   - Server checks if client supports roots protocol (`capabilities.roots`)
   
3. **Roots Protocol Handling** (if client supports roots)
   - **On initialization**: Server requests roots from client via `roots/list`
   - Client responds with its configured roots
   - Server replaces ALL allowed directories with client's roots
   - **On runtime updates**: Client can send `notifications/roots/list_changed`
   - Server requests updated roots and replaces allowed directories again

4. **Fallback Behavior** (if client doesn't support roots)
   - Server continues using command-line directories only
   - No dynamic updates possible

5. **Access Control**
   - All filesystem operations are restricted to allowed directories
   - Use `list_allowed_directories` tool to see current directories
   - Server requires at least ONE allowed directory to operate

**Note**: The server will only allow operations within directories specified either via `args` or via Roots.



## API

### Resources

- `file://system`: File system operations interface

### Tools

- **read_file**
  - Read complete contents of a file
  - Input: `path` (string)
  - Reads complete file contents with UTF-8 encoding

- **read_multiple_files**
  - Read multiple files simultaneously
  - Input: `paths` (string[])
  - Failed reads won't stop the entire operation

- **write_file**
  - Create new file or overwrite existing (exercise caution with this)
  - Inputs:
    - `path` (string): File location
    - `content` (string): File content

- **edit_file**
  - Make selective edits using advanced pattern matching and formatting
  - Features:
    - Line-based and multi-line content matching
    - Whitespace normalization with indentation preservation
    - Multiple simultaneous edits with correct positioning
    - Indentation style detection and preservation
    - Git-style diff output with context
    - Preview changes with dry run mode
  - Inputs:
    - `path` (string): File to edit
    - `edits` (array): List of edit operations
      - `oldText` (string): Text to search for (can be substring)
      - `newText` (string): Text to replace with
    - `dryRun` (boolean): Preview changes without applying (default: false)
  - Returns detailed diff and match information for dry runs, otherwise applies changes
  - Best Practice: Always use dryRun first to preview changes before applying them

- **create_directory**
  - Create new directory or ensure it exists
  - Input: `path` (string)
  - Creates parent directories if needed
  - Succeeds silently if directory exists

- **list_directory**
  - List directory contents with [FILE] or [DIR] prefixes
  - Input: `path` (string)

- **move_file**
  - Move or rename files and directories
  - Inputs:
    - `source` (string)
    - `destination` (string)
  - Fails if destination exists

- **search_files**
  - Recursively search for files/directories
  - Inputs:
    - `path` (string): Starting directory
    - `pattern` (string): Search pattern
    - `excludePatterns` (string[]): Exclude any patterns. Glob formats are supported.
  - Case-insensitive matching
  - Returns full paths to matches

- **get_file_info**
  - Get detailed file/directory metadata
  - Input: `path` (string)
  - Returns:
    - Size
    - Creation time
    - Modified time
    - Access time
    - Type (file/directory)
    - Permissions

- **list_allowed_directories**
  - List all directories the server is allowed to access
  - No input required
  - Returns:
    - Directories that this server can read/write from

## Usage with Claude Desktop
Add this to your `claude_desktop_config.json`:

Note: you can provide sandboxed directories to the server by mounting them to `/projects`. Adding the `ro` flag will make the directory readonly by the server.

### Docker
Note: all directories must be mounted to `/projects` by default.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--mount", "type=bind,src=/Users/username/Desktop,dst=/projects/Desktop",
        "--mount", "type=bind,src=/path/to/other/allowed/dir,dst=/projects/other/allowed/dir,ro",
        "--mount", "type=bind,src=/path/to/file.txt,dst=/projects/path/to/file.txt",
        "mcp/filesystem",
        "/projects"
      ]
    }
  }
}
```

### NPX

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/path/to/other/allowed/dir"
      ]
    }
  }
}
```

## Usage with VS Code

For quick installation, click the installation buttons below...

[![Install with NPX in VS Code](https://img.shields.io/badge/VS_Code-NPM-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=filesystem&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40modelcontextprotocol%2Fserver-filesystem%22%2C%22%24%7BworkspaceFolder%7D%22%5D%7D) [![Install with NPX in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-NPM-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=filesystem&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40modelcontextprotocol%2Fserver-filesystem%22%2C%22%24%7BworkspaceFolder%7D%22%5D%7D&quality=insiders)

[![Install with Docker in VS Code](https://img.shields.io/badge/VS_Code-Docker-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=filesystem&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22--mount%22%2C%22type%3Dbind%2Csrc%3D%24%7BworkspaceFolder%7D%2Cdst%3D%2Fprojects%2Fworkspace%22%2C%22mcp%2Ffilesystem%22%2C%22%2Fprojects%22%5D%7D) [![Install with Docker in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Docker-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=filesystem&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22--mount%22%2C%22type%3Dbind%2Csrc%3D%24%7BworkspaceFolder%7D%2Cdst%3D%2Fprojects%2Fworkspace%22%2C%22mcp%2Ffilesystem%22%2C%22%2Fprojects%22%5D%7D&quality=insiders)

For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `Preferences: Open Settings (JSON)`.

Optionally, you can add it to a file called `.vscode/mcp.json` in your workspace. This will allow you to share the configuration with others.

> Note that the `mcp` key is not needed in the `.vscode/mcp.json` file.

You can provide sandboxed directories to the server by mounting them to `/projects`. Adding the `ro` flag will make the directory readonly by the server.

### Docker
Note: all directories must be mounted to `/projects` by default. 

```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "docker",
        "args": [
          "run",
          "-i",
          "--rm",
          "--mount", "type=bind,src=${workspaceFolder},dst=/projects/workspace",
          "mcp/filesystem",
          "/projects"
        ]
      }
    }
  }
}
```

### NPX

```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": [
          "-y",
          "@modelcontextprotocol/server-filesystem",
          "${workspaceFolder}"
        ]
      }
    }
  }
}
```

## Build

Docker build:

```bash
docker build -t mcp/filesystem -f src/filesystem/Dockerfile .
```

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.

--- END OF FILE README.md ---


--- START OF FILE roots-utils.ts ---
import { promises as fs, type Stats } from 'fs';
import path from 'path';
import os from 'os';
import { normalizePath } from './path-utils.js';
import type { Root } from '@modelcontextprotocol/sdk/types.js';

/**
 * Converts a root URI to a normalized directory path with basic security validation.
 * @param rootUri - File URI (file://...) or plain directory path
 * @returns Promise resolving to validated path or null if invalid
 */
async function parseRootUri(rootUri: string): Promise<string | null> {
  try {
    const rawPath = rootUri.startsWith('file://') ? rootUri.slice(7) : rootUri;
    const expandedPath = rawPath.startsWith('~/') || rawPath === '~' 
      ? path.join(os.homedir(), rawPath.slice(1)) 
      : rawPath;
    const absolutePath = path.resolve(expandedPath);
    const resolvedPath = await fs.realpath(absolutePath);
    return normalizePath(resolvedPath);
  } catch {
    return null; // Path doesn't exist or other error
  }
}

/**
 * Formats error message for directory validation failures.
 * @param dir - Directory path that failed validation
 * @param error - Error that occurred during validation
 * @param reason - Specific reason for failure
 * @returns Formatted error message
 */
function formatDirectoryError(dir: string, error?: unknown, reason?: string): string {
  if (reason) {
    return `Skipping ${reason}: ${dir}`;
  }
  const message = error instanceof Error ? error.message : String(error);
  return `Skipping invalid directory: ${dir} due to error: ${message}`;
}

/**
 * Resolves requested root directories from MCP root specifications.
 * 
 * Converts root URI specifications (file:// URIs or plain paths) into normalized
 * directory paths, validating that each path exists and is a directory.
 * Includes symlink resolution for security.
 * 
 * @param requestedRoots - Array of root specifications with URI and optional name
 * @returns Promise resolving to array of validated directory paths
 */
export async function getValidRootDirectories(
  requestedRoots: readonly Root[]
): Promise<string[]> {
  const validatedDirectories: string[] = [];
  
  for (const requestedRoot of requestedRoots) {
    const resolvedPath = await parseRootUri(requestedRoot.uri);
    if (!resolvedPath) {
      console.error(formatDirectoryError(requestedRoot.uri, undefined, 'invalid path or inaccessible'));
      continue;
    }
    
    try {
      const stats: Stats = await fs.stat(resolvedPath);
      if (stats.isDirectory()) {
        validatedDirectories.push(resolvedPath);
      } else {
        console.error(formatDirectoryError(resolvedPath, undefined, 'non-directory root'));
      }
    } catch (error) {
      console.error(formatDirectoryError(resolvedPath, error));
    }
  }
  
  return validatedDirectories;
}
--- END OF FILE roots-utils.ts ---


--- START OF FILE tsconfig.json ---
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": ".",
    "moduleResolution": "NodeNext",
    "module": "NodeNext"
  },
  "include": [
    "./**/*.ts"
  ]
}

--- END OF FILE tsconfig.json ---



--- PROJECT PACKAGING COMPLETE ---