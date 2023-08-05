"""faligning comments and variable declarations."""
from typing import List, Optional


class FAlign:
    """Aligning comments and sometimes variable declarations."""

    def __init__(self, min_space_before_comment: int = 1,
                 comment_start_column: Optional[int] = None,
                 ignore_offset: Optional[int] = None):
        self.min_space_before_comment = min_space_before_comment
        self.comment_start_column = comment_start_column
        self.ignore_offset = ignore_offset

    def falign(self, lines: List[str]) -> List[str]:
        """aligns input file and writes to output file."""

        output_lines: List[str] = []
        block_slice: slice = slice(None)
        while True:
            block_slice = self.next_block_slice(block_slice.stop, lines)
            if block_slice.start is None:
                break

            # Determine the code indent at the start of the next block for
            # trailing comments and comments outside a block
            next_block_code_indent: Optional[int] = None
            next_block_slice: slice = block_slice
            while next_block_code_indent is None:
                next_block_slice = \
                    self.next_block_slice(next_block_slice.stop, lines)
                if next_block_slice.start is None:
                    break
                else:
                    next_block_code_indent = \
                        FAlign._code_indent(lines[next_block_slice])

            block = lines[block_slice]
            self._align_block_comments(block, next_block_code_indent)
            output_lines.extend(block)

        return output_lines

    def _align_block_comments(self, lines: List[str],
                              next_block_code_indent: Optional[int] = None
                              ) -> None:
        to_align: List[int] = []
        align_index: int = 0 if self.comment_start_column is None \
            or self.comment_start_column <= 0 \
            else self.comment_start_column - 1

        # Remember if the last line had code and comment
        last_line_post_code_comment: bool = False
        current_line_post_code_comment: bool = False

        # Remember the code length of the last line
        last_line_code_length: int = 0
        current_line_code_length: int = 0

        # Remember the code indent
        last_line_code_indent: Optional[int] = None
        current_line_code_indent: Optional[int] = None

        for iline, line in enumerate(lines):
            last_line_post_code_comment = current_line_post_code_comment
            current_line_post_code_comment = False

            last_line_code_length = current_line_code_length
            current_line_code_length = 0

            last_line_code_indent = current_line_code_indent
            # current_line_code_indent = None
            current_line_code_indent = self._code_indent(lines[iline:iline])

            current_line_comment_index: Optional[int] = self._comment_index(line)

            # Leave comments without indentation at the beginning
            if current_line_comment_index is None or current_line_comment_index == 0:
                continue

            # Check whether the align_index is huge enough to fit the
            # minimal ammount of requestet spaces (min_space_before_comment)
            # before the start of the comment.
            # If not increment the align_index.
            current_line_code_length = len(line[:current_line_comment_index].rstrip())
            if current_line_code_length + self.min_space_before_comment > align_index:
                align_index = current_line_code_length + self.min_space_before_comment

            # Check wheter the line has code and a post code comment and
            # remember it for later
            if current_line_comment_index is not None and \
                    current_line_code_length is not None and \
                    current_line_comment_index > 0 and \
                    current_line_code_length > 0:
                current_line_post_code_comment = True
            else:
                current_line_post_code_comment = False

            # Comment line following a code line with a comment
            # gets the comments aligned. Even if it is a comment only line!
            # int(2) :: i ! Comment
            #             ! Comment line following a code line w/ comment
            if current_line_comment_index is not None and \
                    current_line_comment_index > 0 and \
                    last_line_post_code_comment:
                current_line_post_code_comment = True
                pass
            # Comment only line
            elif self._first_non_whitespace(lines[iline]) == '!':
                # Comments following a line of code get the same indentation
                #     call test()
                #     ! Comment line following a code line w/o comment
                #print(f"{last_line_code_indent}")
                #if last_line_code_indent is not None:
                #    lines[iline] = ' ' * last_line_code_indent + \
                #                   lines[iline][current_line_comment_index:]
                #    current_line_code_indent = last_line_code_indent
                #    continue

                current_line_code_indent = self._code_indent(lines[iline:])

                # If we could not determine the code indent of the next line
                # of code use the one found in the next block
                if current_line_code_indent is None:
                    current_line_code_indent = next_block_code_indent

                indent = current_line_code_indent if self.ignore_offset is None else \
                    current_line_code_indent + self.ignore_offset + 1

                # Fix comments which belong to code and are not indented enough
                if current_line_code_indent is not None and 0 < current_line_comment_index < indent:
                    lines[iline] = ' ' * current_line_code_indent + \
                                   lines[iline][current_line_comment_index:]
                    continue
                # Ignore comments which belong to code and are on
                # code indention
                elif current_line_comment_index == current_line_code_indent:
                    continue
                # Align comments whose indent is greater than
                # current code indent
                else:
                    pass

            to_align.append(iline)

        for iline in to_align:
            current_line_comment_index = self._comment_index(lines[iline])

            if current_line_comment_index is None or current_line_comment_index == 0:
                continue

            comment = lines[iline][current_line_comment_index:]
            code = lines[iline][:current_line_comment_index].rstrip()
            current_line_code_length = len(code)

            lines[iline] = code \
                + ' ' * (align_index - current_line_code_length) \
                + comment

    @staticmethod
    def _code_indent(lines: List[str]) -> Optional[int]:
        """Gives the current indent of the current line of code, if the current
        line contains no code looks for the next line of code."""

        for iline, _ in enumerate(lines):
            if FAlign._is_empty(lines[iline]):
                continue
            inws: Optional[int] = FAlign._first_non_whitespace_index(
                lines[iline])
            if inws is None:
                continue
            if lines[iline][inws] == '!':
                continue
            return inws
        return None

    @staticmethod
    def _comment_index(line: str) -> Optional[int]:
        string_delimiter: Optional[str] = None

        for iline, _ in enumerate(line):
            char = line[iline]

            if string_delimiter and char != string_delimiter:
                continue

            if string_delimiter and char == string_delimiter:
                string_delimiter = None
                continue

            if char in ('\'', '"'):
                string_delimiter = char
                continue

            if char == '!':
                return iline

        return None

    @staticmethod
    def _first_non_whitespace(line: str) -> Optional[str]:
        i = FAlign._first_non_whitespace_index(line)
        return None if i is None else line[i]

    @staticmethod
    def _first_non_whitespace_index(line: str) -> Optional[int]:
        for iline, _ in enumerate(line):
            if line[iline].strip():
                return iline

        return None

    @staticmethod
    def next_block_slice(current: Optional[int], lines: List[str]) \
            -> slice:
        """Finds next block of code and includes leading and trailing empty
        lines."""

        if not current:
            start = 0
        elif current < 0:
            start = 0
        else:
            start = current

        if current is not None and current >= len(lines):
            return slice(None)

        end = start

        # Find end of block
        while True:
            # End of list
            if end >= len(lines):
                return slice(start, end)

            # Empty line --> search for start of next block --> end of block
            if FAlign._is_empty(lines[end]):
                # Find first non empty line and include trailing empty lines
                while True:
                    # End of list
                    if end >= len(lines):
                        return slice(start, end)

                    # Non empty line --> End of block
                    if not FAlign._is_empty(lines[end]):
                        return slice(start, end)

                    end = end + 1

            end = end + 1

    @staticmethod
    def _is_empty(string: str) -> bool:
        return not string.strip()
